
import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput # 🌟 新增這行：載入介面套件
import discord
from flask import Flask
from threading import Thread
from discord.ext import commands
import requests
import urllib.parse
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
from dotenv import load_dotenv
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
    if "憨仔" in message.content:
        # 1. 建立一個乾淨的無字框架
        embed = discord.Embed()
        # 2. 把你的 GIF 網址塞進這個框架的圖片區
        embed.set_image(url="https://s1.aigei.com/src/img/gif/46/46a1b81cde50407982da18d76b651dcf.gif?e=2051020800&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:K5m3jpqMlPrNV-mjz5ONf9znTOw=")
        
        # 3. 發送文字，並且「同時」附上這個乾淨的圖片框架！
        await message.channel.send("除聖傑說柯柏宏是憨仔", embed=embed)

    # ⚠️ 最重要的一行：確保機器人處理完關鍵字後，不會忘記執行 ! 開頭的指令
    await bot.process_commands(message)


# ==========================================
# 5. 特戰英豪主打商店組合包查詢 (終極圖文進化版)
# ==========================================
@bot.command()
async def bundle(ctx):
    await ctx.send("🔍 正在連線至 Riot 商店與圖庫獲取最新資訊...")
    
    try:
        import requests 
        import discord # 引入 discord 套件來製作漂亮的圖文框
        
        # --- 步驟 1：向 Riot 商店伺服器要「商品條碼」與「價格」 ---
        url = "https://api.henrikdev.xyz/valorant/v1/store-featured"
        headers = {"Authorization": API_KEY} 
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('data'):
                api_data = data['data']
                
                if isinstance(api_data, list) and len(api_data) > 0:
                    bundle_info = api_data[0]
                elif isinstance(api_data, dict):
                    bundle_info = api_data
                else:
                    await ctx.send("❌ API 回傳的資料格式無法解析。")
                    return
                
                # 抓取物品清單與組合包條碼 (DataAssetID)
                items = []
                bundle_id = ""
                if 'FeaturedBundle' in bundle_info and 'Bundle' in bundle_info['FeaturedBundle']:
                    items = bundle_info['FeaturedBundle']['Bundle'].get('Items', [])
                    bundle_id = bundle_info['FeaturedBundle']['Bundle'].get('DataAssetID', '')
                elif 'Bundle' in bundle_info:
                    items = bundle_info['Bundle'].get('Items', [])
                    bundle_id = bundle_info['Bundle'].get('DataAssetID', '')
                
                if not items:
                    await ctx.send("❌ 成功取得商店資料，但目前架上似乎沒有主打組合包物品。")
                    return
                
                # 計算總價
                total_price = 0
                for item in items:
                    total_price += int(item.get('DiscountedPrice', 0))
                
                # --- 步驟 2：拿著條碼去「圖文素材庫」翻譯成中文名稱與圖片 ---
                bundle_name = "未知主打組合包"
                bundle_image = ""
                
                if bundle_id:
                    # 呼叫開源素材庫，並指定 language=zh-TW 獲取繁體中文
                    asset_url = f"https://valorant-api.com/v1/bundles/{bundle_id}?language=zh-TW"
                    asset_res = requests.get(asset_url, timeout=10)
                    
                    if asset_res.status_code == 200:
                        asset_data = asset_res.json().get('data', {})
                        bundle_name = asset_data.get('displayName', bundle_name)
                        bundle_image = asset_data.get('displayIcon', '') # 抓取官方宣傳圖網址
                
                # --- 步驟 3：製作專業的 Discord 圖文框 (Embed) ---
                embed = discord.Embed(
                    title=f"✨ 本期主打：【 {bundle_name} 】", 
                    description="趕快登入遊戲查看詳細內容吧！",
                    color=0xFF4655 # 使用特戰英豪的經典紅色
                )
                embed.add_field(name="💰 總價格", value=f"**{total_price} VP**", inline=False)
                
                # 如果有抓到圖片，就把它塞進圖文框裡
                if bundle_image:
                    embed.set_image(url=bundle_image)
                
                # 發送精美圖文！
                await ctx.send(embed=embed)
                
            else:
                await ctx.send("❌ 目前 API 沒有回傳任何主打組合包資料！")
                
        elif response.status_code in [401, 403]:
            await ctx.send("❌ 存取被拒！請檢查你的 API 金鑰是否正確。")
        else:
            await ctx.send(f"❌ 抓取失敗，伺服器狀態碼：{response.status_code}")
            
    except Exception as e:
        print(f"組合包查詢錯誤: {repr(e)}") 
        await ctx.send(f"⚠️ 發生系統錯誤，請查看 Render 日誌。")
# ==========================================
# 8. 尊爵會員專屬：能力雷達圖 (5場平均 + 中文顯示版)
# ==========================================
@bot.command()
async def radar(ctx, *, riot_id: str = None):
    if riot_id is None or '#' not in riot_id:
        await ctx.send("⚠️ 格式錯誤！請輸入完整的 Riot ID，例如：`!radar 玩家名稱#TW1`")
        return

    parts = riot_id.split('#', 1)
    name = parts[0].strip()
    tag = parts[1].strip()
    
    await ctx.send(f"📡 正在調閱 **{name}** 最近 5 場的對戰紀錄，進行綜合戰力分析，請稍候...")

    try:
        import urllib.parse
        import urllib.request
        import os
        from matplotlib import font_manager

        # --- 1. 自動下載中文字體 (解決方塊字問題) ---
        font_path = 'NotoSansTC.otf'
        if not os.path.exists(font_path):
            print("DEBUG: 正在下載中文字體...")
            # 從 Google Fonts 開源庫下載思源黑體
            font_url = 'https://raw.githubusercontent.com/googlefonts/noto-cjk/main/Sans/OTF/TraditionalChinese/NotoSansCJKtc-Regular.otf'
            urllib.request.urlretrieve(font_url, font_path)
        
        # 載入字體設定
        my_font = font_manager.FontProperties(fname=font_path)

        # --- 2. 抓取最近 5 場戰績 ---
        encoded_name = urllib.parse.quote(name)
        encoded_tag = urllib.parse.quote(tag)
        
        # ⚠️ 關鍵：將 size=1 改為 size=5
        match_url = f"https://api.henrikdev.xyz/valorant/v3/matches/ap/{encoded_name}/{encoded_tag}?size=5"
        
        headers = {
            "Authorization": API_KEY
        }
        
        match_response = requests.get(match_url, headers=headers, timeout=15)
        
        if match_response.status_code != 200:
            print(f"DEBUG: 抓戰績失敗，狀態碼: {match_response.status_code}")
            await ctx.send(f"❌ 查無戰績或通行證失效 (API 狀態碼 {match_response.status_code})。")
            return
            
        matches = match_response.json().get('data')
        if not matches:
            await ctx.send("❌ 該帳號查無近期對戰紀錄，無法繪製雷達圖。")
            return

        # --- 3. 數據萃取與平均計算 ---
        match_count = len(matches) # 實際抓到的場數 (最高5場)
        total_kills = 0
        total_assists = 0
        total_score = 0
        total_headshots = 0
        total_shots = 0

        # 用迴圈把每一場的數據加總起來
        for match in matches:
            for p in match['players']['all_players']:
                if p['name'].lower() == name.lower():
                    stats = p['stats']
                    total_kills += stats.get('kills', 0)
                    total_assists += stats.get('assists', 0)
                    total_score += stats.get('score', 0)
                    
                    headshots = stats.get('headshots', 0)
                    bodyshots = stats.get('bodyshots', 0)
                    legshots = stats.get('legshots', 0)
                    total_headshots += headshots
                    total_shots += (headshots + bodyshots + legshots)
                    break

        # 計算平均值
        avg_kills = total_kills / match_count
        avg_assists = total_assists / match_count
        avg_score = total_score / match_count
        headshot_percent = (total_headshots / total_shots) * 100 if total_shots > 0 else 0

        # --- 4. 數據轉換引擎 (0-100 分) ---
        # 為了平均值，稍微下修滿分標準 (例如場均 25 殺即滿分)
        score_kills = min(100, (avg_kills / 25) * 100) 
        score_assists = min(100, (avg_assists / 10) * 100)
        score_hs = min(100, (headshot_percent / 40) * 100)
        score_combat = min(100, (avg_score / 6000) * 100) 
        score_overall = (score_kills + score_assists + score_hs + score_combat) / 4

        # --- 5. 啟動繪圖引擎 ---
        # 換回霸氣的中文標籤
        categories = ['擊殺爆發力', '團隊助攻', '精準爆頭率', '戰鬥總分', '綜合表現']
        values = [score_kills, score_assists, score_hs, score_combat, score_overall]

        N = len(categories)
        angles = [n / float(N) * 2 * math.pi for n in range(N)]
        angles += angles[:1]
        values += values[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.plot(angles, values, color='#FF4655', linewidth=2, linestyle='solid')
        ax.fill(angles, values, color='#FF4655', alpha=0.4)

        # ⚠️ 關鍵：套用下載好的 my_font 中文字體
        plt.xticks(angles[:-1], categories, fontsize=12, color='black', fontproperties=my_font)
        ax.set_yticklabels([])
        
        # 標題也套用中文字體，並標示計算了幾場
        title_text = f"【 {name} 】近 {match_count} 場平均戰力分析"
        plt.title(title_text, size=18, weight='bold', color='#333333', y=1.1, fontproperties=my_font)

        file_name = 'radar_chart.png'
        plt.savefig(file_name, bbox_inches='tight')
        plt.close() 

        # --- 6. 發送到 Discord ---
        picture = discord.File(file_name)
        msg = (f"✨ {ctx.author.mention}，戰力分析完成！\n"
               f"基於最近 **{match_count}** 場對戰數據：\n"
               f"場均擊殺：**{avg_kills:.1f}** 殺\n"
               f"平均爆頭率：**{headshot_percent:.1f}%**")
        await ctx.send(msg, file=picture)

    except Exception as e:
        print(f"雷達圖系統錯誤: {e}")
        await ctx.send("⚠️ 系統發生錯誤，請稍後再試。")
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
# ==========================================
# 9. 互動式圖形介面：戰術終端機選單 (完全合體版)
# ==========================================

# --- 步驟 A：彈出視窗 (負責畫雷達圖) ---
class RadarModal(Modal, title='📊 查詢戰績雷達圖'):
    riot_id_input = TextInput(
        label='請輸入您的 Riot ID',
        placeholder='例如：絕境大蕃薯#0313',
        required=True,
        max_length=30
    )

    async def on_submit(self, interaction: discord.Interaction):
        # 1. 爭取時間：先發送一條訊息，避免 3 秒超時
        await interaction.response.send_message(f"📡 正在為 `{self.riot_id_input.value}` 讀取近 5 場戰績並生成雷達圖，請稍候...", ephemeral=False)
        
        riot_id = self.riot_id_input.value
        name, tag = riot_id.split('#')[0].strip(), riot_id.split('#')[1].strip() if '#' in riot_id else ("", "")
        
        if not name or not tag:
            await interaction.followup.send("⚠️ 格式錯誤！請輸入完整的 Riot ID，例如：玩家名稱#TW1")
            return

        try:
            import urllib.parse
            import urllib.request
            import os
            from matplotlib import font_manager
            import matplotlib.pyplot as plt
            import math
            import requests

            # 下載字體
            font_path = 'NotoSansTC.otf'
            if not os.path.exists(font_path):
                font_url = 'https://raw.githubusercontent.com/googlefonts/noto-cjk/main/Sans/OTF/TraditionalChinese/NotoSansCJKtc-Regular.otf'
                urllib.request.urlretrieve(font_url, font_path)
            my_font = font_manager.FontProperties(fname=font_path)

            # 抓取 5 場戰績
            encoded_name, encoded_tag = urllib.parse.quote(name), urllib.parse.quote(tag)
            match_url = f"https://api.henrikdev.xyz/valorant/v3/matches/ap/{encoded_name}/{encoded_tag}?size=5"
            headers = {"Authorization": API_KEY}
            match_response = requests.get(match_url, headers=headers, timeout=15)
            
            if match_response.status_code == 200:
                matches = match_response.json().get('data')
                if not matches:
                    await interaction.followup.send("❌ 該帳號查無近期對戰紀錄。")
                    return

                # 計算平均
                match_count = len(matches)
                total_kills, total_assists, total_score, total_headshots, total_shots = 0, 0, 0, 0, 0
                for match in matches:
                    for p in match['players']['all_players']:
                        if p['name'].lower() == name.lower():
                            stats = p['stats']
                            total_kills += stats.get('kills', 0)
                            total_assists += stats.get('assists', 0)
                            total_score += stats.get('score', 0)
                            total_headshots += stats.get('headshots', 0)
                            total_shots += (stats.get('headshots', 0) + stats.get('bodyshots', 0) + stats.get('legshots', 0))
                            break

                avg_kills = total_kills / match_count
                avg_assists = total_assists / match_count
                avg_score = total_score / match_count
                headshot_percent = (total_headshots / total_shots) * 100 if total_shots > 0 else 0

                # 畫圖
                score_kills = min(100, (avg_kills / 25) * 100) 
                score_assists = min(100, (avg_assists / 10) * 100)
                score_hs = min(100, (headshot_percent / 40) * 100)
                score_combat = min(100, (avg_score / 6000) * 100) 
                score_overall = (score_kills + score_assists + score_hs + score_combat) / 4

                categories = ['擊殺爆發力', '團隊助攻', '精準爆頭率', '戰鬥總分', '綜合表現']
                values = [score_kills, score_assists, score_hs, score_combat, score_overall]
                N = len(categories)
                angles = [n / float(N) * 2 * math.pi for n in range(N)]
                angles += angles[:1]
                values += values[:1]

                fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
                ax.plot(angles, values, color='#FF4655', linewidth=2, linestyle='solid')
                ax.fill(angles, values, color='#FF4655', alpha=0.4)
                plt.xticks(angles[:-1], categories, fontsize=12, color='black', fontproperties=my_font)
                ax.set_yticklabels([])
                plt.title(f"【 {name} 】近 {match_count} 場平均戰力分析", size=18, weight='bold', color='#333333', y=1.1, fontproperties=my_font)

                file_name = 'radar_chart.png'
                plt.savefig(file_name, bbox_inches='tight')
                plt.close() 

                # 2. 由於前面已經 send_message，這裡必須用 followup.send 來補發圖片
                picture = discord.File(file_name)
                msg = (f"✨ {interaction.user.mention}，戰力分析完成！\n"
                       f"場均擊殺：**{avg_kills:.1f}** 殺 │ 平均爆頭率：**{headshot_percent:.1f}%**")
                await interaction.followup.send(content=msg, file=picture)
            else:
                await interaction.followup.send(f"❌ 查無戰績 (狀態碼 {match_response.status_code})。")
        except Exception as e:
            print(f"雷達圖按鈕錯誤: {e}")
            await interaction.followup.send("⚠️ 系統發生錯誤，請稍後再試。")

# --- 步驟 B：按鈕選單 (負責商店與呼叫雷達圖) ---
class ValoMenu(View):
    def __init__(self):
        super().__init__(timeout=None) 

    # 🛍️ 商店按鈕
    @discord.ui.button(label="查看今日組合包", style=discord.ButtonStyle.blurple, emoji="🛍️")
    async def bundle_btn(self, interaction: discord.Interaction, button: Button):
        # 1. 爭取時間 (因為我們沒有要彈出視窗，所以用 defer)
        await interaction.response.defer(ephemeral=False)
        
        try:
            import requests 
            import discord 
            
            url = "https://api.henrikdev.xyz/valorant/v1/store-featured"
            headers = {"Authorization": API_KEY} 
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                bundle_info = response.json()['data'][0] if isinstance(response.json()['data'], list) else response.json()['data']
                items = bundle_info.get('FeaturedBundle', {}).get('Bundle', {}).get('Items', []) or bundle_info.get('Bundle', {}).get('Items', [])
                bundle_id = bundle_info.get('FeaturedBundle', {}).get('Bundle', {}).get('DataAssetID', '') or bundle_info.get('Bundle', {}).get('DataAssetID', '')
                
                total_price = sum(int(item.get('DiscountedPrice', 0)) for item in items)
                
                bundle_name, bundle_image = "未知主打組合包", ""
                if bundle_id:
                    asset_res = requests.get(f"https://valorant-api.com/v1/bundles/{bundle_id}?language=zh-TW", timeout=10)
                    if asset_res.status_code == 200:
                        bundle_name = asset_res.json().get('data', {}).get('displayName', bundle_name)
                        bundle_image = asset_res.json().get('data', {}).get('displayIcon', '') 
                
                embed = discord.Embed(title=f"✨ 本期主打：【 {bundle_name} 】", description="趕快登入遊戲查看詳細內容吧！", color=0xFF4655)
                embed.add_field(name="💰 總價格", value=f"**{total_price} VP**", inline=False)
                if bundle_image: embed.set_image(url=bundle_image)
                
                # 2. 處理完畢，補發圖文框給玩家
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send("❌ 抓取商店失敗。")
        except Exception as e:
            print(f"商店按鈕錯誤: {e}")
            await interaction.followup.send("⚠️ 系統發生錯誤。")

    # 🎯 戰績按鈕
    @discord.ui.button(label="生成雷達圖", style=discord.ButtonStyle.red, emoji="🎯")
    async def radar_btn(self, interaction: discord.Interaction, button: Button):
        # 呼叫並彈出 RadarModal 視窗
        await interaction.response.send_modal(RadarModal())

# --- 步驟 C：觸發選單的指令 ---
@bot.command()
async def menu(ctx):
    embed = discord.Embed(
        title="🎮 特戰英豪戰術終端機",
        description="歡迎使用系統！請點擊下方的按鈕來操作：\n\n🛍️ **查看今日組合包**：顯示目前架上的主打商品\n🎯 **生成雷達圖**：輸入 ID 查詢近 5 場戰力平均",
        color=0x2b2d31 
    )
    await ctx.send(embed=embed, view=ValoMenu())

bot.run(TOKEN)