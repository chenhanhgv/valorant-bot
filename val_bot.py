import discord
from discord.ext import commands
import requests
import urllib.parse
import os # 【新增】跟系統溝通的工具
from dotenv import load_dotenv # 【新增】讀取密碼本的工具

# 讓程式去讀取我們剛剛建立的 .env 檔案
load_dotenv()

# 從密碼本中把密碼抓出來 (取代原本直接寫死在程式碼裡的作法)
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('VALORANT_API_KEY')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'成功登入！特戰特工 {bot.user} 已準備部署！')

# ===== 原有的牌位查詢指令 =====
# 查詢牌位指令：!vgrade 玩家名字#標籤 (例如：!vgrade Tea Latte#0104)
@bot.command()
async def vgrade(ctx, *, riot_id: str):
    try:
        # 切割名字和標籤
        name, tag = riot_id.split('#')
        name = name.strip()
        tag = tag.strip()
    except ValueError:
        await ctx.send("❌ 格式錯誤！請包含 # 符號，例如：`!vgrade Tea Latte#0104`")
        return

    await ctx.send(f"🔍 正在進入特戰資料庫，搜尋特工 {name}#{tag} 的即時戰報...")
    
    # 轉換成網址看得懂的安全格式
    safe_name = urllib.parse.quote(name)
    safe_tag = urllib.parse.quote(tag)
    
    # 呼叫 V1 版本的 API
    url = f"https://api.henrikdev.xyz/valorant/v1/mmr/ap/{safe_name}/{safe_tag}"
    
    # 【新增】：建立通行證夾帶檔案
    headers = {
        "Authorization": API_KEY # 記得換成你的 API Key
    }
    
    try:
        # 【新增】：發送請求時，把 headers 遞交出去
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if response.status_code == 200 and data.get('status') == 200:
            player_data = data['data']
            
            # 解析 V1 API 回傳的資料
            rank = player_data.get('currenttierpatched', '無牌位')
            rr = player_data.get('ranking_in_tier', 0)
            elo = player_data.get('elo', 0)
            
            # 整理回覆訊息
            reply = f"🎮 **【特戰英豪 特工戰報】** 🎮\n"
            reply += f"👤 **玩家：** {name}#{tag}\n"
            reply += f"🏅 **目前牌位：** {rank}\n"
            reply += f"📈 **當前分數：** {rr} RR\n"
            reply += f"🔥 **隱藏積分：** {elo}"
            
            await ctx.send(reply)
        else:
            error_status = data.get('status', response.status_code)
            await ctx.send(f"❌ 查詢失敗！錯誤代碼：`{error_status}`\n(可能原因：這季還沒打過競技模式、帳號不存在，或伺服器維護中)")
            print(f"API 錯誤回應: {data}")
            
    except Exception as e:
        await ctx.send("⚠️ 系統連線失敗，請稍後再試。")

# ===== 【新增】歷史戰績查詢指令 =====
# 使用方式：!vhistory 玩家名字#標籤
@bot.command()
async def vhistory(ctx, *, riot_id: str):
    try:
        name, tag = riot_id.split('#')
        name = name.strip()
        tag = tag.strip()
    except ValueError:
        await ctx.send("❌ 格式錯誤！請包含 # 符號，例如：`!vhistory Tea Latte#0104`")
        return

    await ctx.send(f"📊 正在從戰場伺服器下載 {name}#{tag} 的最新對戰紀錄...")
    
    safe_name = urllib.parse.quote(name)
    safe_tag = urllib.parse.quote(tag)
    
    url = f"https://api.henrikdev.xyz/valorant/v3/matches/ap/{safe_name}/{safe_tag}?size=1"
    
    # 建立通行證夾帶檔案 (Headers)
    headers = {
        "Authorization": API_KEY
    }
    
    try:
        # 發送請求時，把通行證 (headers) 一起遞交給警衛
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if response.status_code == 200 and data.get('status') == 200 and data.get('data'):
            # 拿到最新的一場比賽資料
            latest_match = data['data'][0]
            metadata = latest_match['metadata']
            
            game_map = metadata.get('map', '未知地圖')
            game_mode = metadata.get('mode', '未知模式')
            
            # 在這場比賽的 10 位玩家中，用迴圈找出「你」的數據
            player_stats = None
            for player in latest_match['players']['all_players']:
                if player['name'].lower() == name.lower():
                    player_data = player
                    break
            
            if player_data:
                agent = player_data.get('character', '未知角色')
                stats = player_data.get('stats', {})
                kills = stats.get('kills', 0)
                deaths = stats.get('deaths', 0)
                assists = stats.get('assists', 0)
                
                # 計算 KDA 數據
                kda_ratio = round((kills + assists) / max(deaths, 1), 2)
                
                # 整理戰報訊息
                reply = f"⚔️ **【特戰英豪 最近戰績】** ⚔️\n"
                reply += f"👤 **特工：** {name}#{tag}\n"
                reply += f"🗺️ **對戰地圖：** {game_map} ({game_mode})\n"
                reply += f"👤 **使用英雄：** {agent}\n"
                reply += f"📊 **本局戰績 (K/D/A)：** {kills} / {deaths} / {assists}\n"
                reply += f"🔥 **KDA 綜合評分：** {kda_ratio}"
                
                await ctx.send(reply)
            else:
                await ctx.send("❌ 成功抓取對戰紀錄，但在該場比賽中找不到您的核心資料。")
        else:
            await ctx.send("❌ 無法抓取歷史紀錄，請確認該帳號近期是否有進行對戰。")
            
    except Exception as e:
        print(f"錯誤訊息: {e}")
        await ctx.send("⚠️ 讀取歷史資料失敗，請稍後再試。")

bot.run(TOKEN)