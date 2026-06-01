import discord
from flask import Flask
from threading import Thread
from discord.ext import commands
import requests
import urllib.parse
import os # 【新增】跟系統溝通的工具
from dotenv import load_dotenv # 【新增】讀取密碼本的工具
# 建立一個迷你的網頁伺服器來欺騙 Render
app = Flask('')

@app.route('/')
def home():
    return "特戰機器人正在雲端守護伺服器！"

def run_server():
    # 綁定 8080 讓 Render 以為這是一個正常的網站
    app.run(host='0.0.0.0', port=8080)

# 在背景啟動這個假網頁
Thread(target=run_server).start()


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
@bot.event
async def on_message(message):
    # 避免機器人自己回覆自己而無限迴圈
    if message.author == bot.user:
        return

    # 關鍵字 1：純文字精準回覆
    if message.content == "早安":
        await message.channel.send(f"早安啊 {message.author.mention}！今天準備好爬分了嗎？")

    # 關鍵字 2：包含特定字眼就觸發
    if "VAN9001" in message.content or "防作弊" in message.content:
        await message.channel.send("又是 Vanguard 搞鬼嗎？重開機治百病啦！")

    # 關鍵字 3：【方法一】文字 + 網路圖片 (GIF動圖)
    if "傻逼" in message.content:
        # 1. 建立一個乾淨的無字框架
        embed = discord.Embed()
        # 2. 把你的 GIF 網址塞進這個框架的圖片區
        embed.set_image(url="https://media1.giphy.com/media/v1.Y2lkPTZjMDliOTUyazNudzN4dWFpbzJjZjRvem13Znc3MWFzcHB5cTc4cTAwZWdhcW5taiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/TKa7fQzChHylCQ89to/200w.gif")
        
        # 3. 發送文字，並且「同時」附上這個乾淨的圖片框架！
        await message.channel.send("誰在找jayyyy", embed=embed)

    # ⚠️ 最重要的一行：確保機器人處理完關鍵字後，不會忘記執行 ! 開頭的指令
    await bot.process_commands(message)


# ==========================================
# 5. 特戰英豪主打商店組合包查詢 (升級防卡死版本)
# ==========================================
@bot.command()
async def bundle(ctx):
    await ctx.send("🔍 正在連線至 Riot 商店獲取最新組合包...")
    
    # 網址修正為最穩定的 v1 版本
    url = "https://api.henrikdev.xyz/valorant/v1/store-featured"
    headers = {"Authorization": VALORANT_API_KEY}
    
    try:
        # 改用 aiohttp，這是非同步套件，不會讓機器人傻等卡死
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                
                # 如果成功抓到資料 (200 OK)
                if response.status == 200:
                    data = await response.json()
                    
                    # 確保 API 裡面真的有放組合包資料
                    if len(data.get('data', [])) > 0:
                        bundle_info = data['data'][0]
                        # 抓取價格，如果 API 沒寫就顯示未知
                        bundle_price = bundle_info.get('bundle_price', '未知')
                        
                        await ctx.send(f"✨ **目前主打組合包！** ✨\n💰 總價格: {bundle_price} 特務幣\n趕快登入遊戲看看吧！")
                    else:
                        await ctx.send("❌ 目前 API 沒有回傳任何主打組合包資料！")
                        
                # 密碼錯誤 (401 或 403)
                elif response.status == 401 or response.status == 403:
                    await ctx.send("❌ 存取被拒！請檢查你的 HDEV API 密碼是否正確。")
                    
                # 其他伺服器錯誤
                else:
                    await ctx.send(f"❌ 抓取失敗，伺服器狀態碼：{response.status}")
                    
    except Exception as e:
        await ctx.send(f"❌ 發生系統錯誤：{e}")
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