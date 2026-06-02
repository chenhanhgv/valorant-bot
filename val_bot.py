
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
# 9. 互動式圖形介面：特戰英豪全功能戰術終端機 (智慧搜尋版)
# ==========================================
import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import urllib.parse
import urllib.request
import os
import requests
import math

# --- 模組 A1：雷達圖視窗 ---
class RadarModal(Modal, title='🎯 查詢戰績雷達圖'):
    riot_id_input = TextInput(label='請輸入 Riot ID (例如：玩家名稱#TW1)', required=True, max_length=30)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"📡 正在生成 `{self.riot_id_input.value}` 的雷達圖，這需要一點時間...", ephemeral=False)
        riot_id = self.riot_id_input.value
        name, tag = riot_id.split('#')[0].strip(), riot_id.split('#')[1].strip() if '#' in riot_id else ("", "")
        
        try:
            from matplotlib import font_manager
            import matplotlib.pyplot as plt

            font_path = 'NotoSansTC.otf'
            if not os.path.exists(font_path):
                urllib.request.urlretrieve('https://raw.githubusercontent.com/googlefonts/noto-cjk/main/Sans/OTF/TraditionalChinese/NotoSansCJKtc-Regular.otf', font_path)
            my_font = font_manager.FontProperties(fname=font_path)

            encoded_name, encoded_tag = urllib.parse.quote(name), urllib.parse.quote(tag)
            match_url = f"https://api.henrikdev.xyz/valorant/v3/matches/ap/{encoded_name}/{encoded_tag}?size=5"
            match_response = requests.get(match_url, headers={"Authorization": API_KEY}, timeout=15)
            
            if match_response.status_code == 200 and match_response.json().get('data'):
                matches = match_response.json()['data']
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

                avg_kills, avg_assists, avg_score = total_kills/match_count, total_assists/match_count, total_score/match_count
                headshot_percent = (total_headshots / total_shots) * 100 if total_shots > 0 else 0

                score_kills, score_assists, score_hs, score_combat = min(100, (avg_kills/25)*100), min(100, (avg_assists/10)*100), min(100, (headshot_percent/40)*100), min(100, (avg_score/6000)*100)
                score_overall = (score_kills + score_assists + score_hs + score_combat) / 4
                categories = ['擊殺爆發力', '團隊助攻', '精準爆頭率', '戰鬥總分', '綜合表現']
                values = [score_kills, score_assists, score_hs, score_combat, score_overall]
                
                angles = [n / float(len(categories)) * 2 * math.pi for n in range(len(categories))]
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

                await interaction.followup.send(content=f"✨ 戰力分析完成！場均擊殺：**{avg_kills:.1f}** 殺 │ 爆頭率：**{headshot_percent:.1f}%**", file=discord.File(file_name))
            else:
                await interaction.followup.send("❌ 查無戰績。")
        except Exception as e:
            await interaction.followup.send(f"⚠️ 系統錯誤：{e}")

# --- 模組 A2：最新對戰紀錄視窗 ---
class HistoryModal(Modal, title='⚔️ 查詢最新對戰紀錄'):
    riot_id_input = TextInput(label='請輸入 Riot ID', required=True, max_length=30)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"🔄 正在調閱 `{self.riot_id_input.value}` 的最新戰報...", ephemeral=False)
        riot_id = self.riot_id_input.value
        name, tag = riot_id.split('#')[0].strip(), riot_id.split('#')[1].strip() if '#' in riot_id else ("", "")
        
        try:
            url = f"https://api.henrikdev.xyz/valorant/v3/matches/ap/{urllib.parse.quote(name)}/{urllib.parse.quote(tag)}?size=1"
            res = requests.get(url, headers={"Authorization": API_KEY}, timeout=10)
            
            if res.status_code == 200 and res.json().get('data'):
                match = res.json()['data'][0]
                meta = match['metadata']
                
                for p in match['players']['all_players']:
                    if p['name'].lower() == name.lower():
                        stats = p['stats']
                        k, d, a = stats.get('kills', 0), stats.get('deaths', 0), stats.get('assists', 0)
                        agent = p.get('character', '未知角色')
                        kda = round((k + a) / max(d, 1), 2)
                        
                        reply = (f"⚔️ **【 {name} 的最新戰報】** ⚔️\n"
                                 f"🗺️ 地圖：{meta.get('map', '未知')} ({meta.get('mode', '未知')})\n"
                                 f"👤 特工：{agent}\n"
                                 f"📊 戰績 (K/D/A)：**{k} / {d} / {a}**\n"
                                 f"🔥 KDA 評分：**{kda}**")
                        await interaction.followup.send(reply)
                        return
                await interaction.followup.send("❌ 在該場比賽中找不到您的資料。")
            else:
                await interaction.followup.send("❌ 查無近期對戰紀錄。")
        except Exception as e:
            await interaction.followup.send(f"⚠️ 讀取失敗。")

# --- 模組 A3：牌位查詢視窗 ---
class RankModal(Modal, title='🏆 查詢目前牌位'):
    riot_id_input = TextInput(label='請輸入 Riot ID', required=True, max_length=30)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"🔍 正在連線 Riot 伺服器查詢牌位...", ephemeral=False)
        riot_id = self.riot_id_input.value
        name, tag = riot_id.split('#')[0].strip(), riot_id.split('#')[1].strip() if '#' in riot_id else ("", "")
        
        try:
            url = f"https://api.henrikdev.xyz/valorant/v1/mmr/ap/{urllib.parse.quote(name)}/{urllib.parse.quote(tag)}"
            res = requests.get(url, headers={"Authorization": API_KEY}, timeout=10)
            
            if res.status_code == 200 and res.json().get('data'):
                data = res.json()['data']
                rank_name = data.get('currenttierpatched', '未知牌位')
                rr = data.get('ranking_in_tier', 0)
                elo = data.get('elo', '未知') 
                
                reply = (f"🏆 **【 {name} 】目前的牌位是：**\n"
                         f"🎖️ 階級：**{rank_name}**\n"
                         f"💯 競技積分 (RR)：**{rr} 分**\n"
                         f"📈 系統總積分 (Elo)：**{elo} 分**")
                await interaction.followup.send(reply)
            else:
                await interaction.followup.send("❌ 查無牌位資料 (可能未打完定級賽)。")
        except Exception as e:
            await interaction.followup.send(f"⚠️ 查詢失敗。")

# --- 🌟 模組 A4：電競賽事智慧搜尋視窗 (Tier 1 頂級賽事過濾版) ---
class EsportsModal(Modal, title='📺 查詢 VCT 電競賽程'):
    team_input = TextInput(
        label='欲查詢的戰隊名稱 (留空則顯示所有近期賽事)', 
        placeholder='例如：PRX 或 SEN (不分大小寫)', 
        required=False, 
        max_length=20
    )

    async def on_submit(self, interaction: discord.Interaction):
        search_team = self.team_input.value.strip().lower()
        
        if search_team:
            await interaction.response.send_message(f"🔍 正在搜尋戰隊 【{self.team_input.value.upper()}】 的近期賽程...", ephemeral=False)
        else:
            await interaction.response.send_message("📡 正在過濾並獲取最新 VCT 【頂級一級賽事】 賽程表...", ephemeral=False)

        try:
            url = "https://vlrggapi.vercel.app/match?q=upcoming"
            res = requests.get(url, timeout=25)
            
            if res.status_code == 200 and res.json().get('data'):
                all_matches = res.json()['data'].get('segments', [])
                
                # 🌟 定義 Tier 1 (頂級賽事) 的關鍵字白名單
                tier1_keywords = ["masters", "champions", "pacific", "americas", "emea", "china"]
                
                filtered_matches = []
                for match in all_matches:
                    # 🌟 防彈升級 1：確保拿到的絕對是字串，才做 .lower()
                    raw_event = str(match.get('match_event') or '').lower()
                    t1 = str(match.get('team1') or 'TBD').lower()
                    t2 = str(match.get('team2') or 'TBD').lower()
                    
                    if search_team:
                        if search_team in t1 or search_team in t2:
                            filtered_matches.append(match)
                    else:
                        is_tier1 = any(kw in raw_event for kw in tier1_keywords)
                        if is_tier1 and "challengers" not in raw_event and "game changers" not in raw_event:
                            filtered_matches.append(match)
                
                if not filtered_matches:
                    msg = f"❌ 抱歉，找不到與「{self.team_input.value}」相關的比賽。" if search_team else "❌ 目前近期內沒有即將開打的 VCT 頂級一級賽事。"
                    await interaction.followup.send(msg)
                    return

                display_matches = filtered_matches[:5]
                
                embed = discord.Embed(
                    title="📺 VCT 頂級職業賽程表" if not search_team else f"📺 【{self.team_input.value.upper()}】 專屬賽程篩選結果",
                    description="資料即時連線自 VLR.gg 數據庫",
                    color=0x9b59b6
                )
                
                def translate_terms(text):
                    terms = {
                        "Masters": "大師賽",
                        "Champions": "世界冠軍賽",
                        "Challengers": "挑戰者聯賽",
                        "Playoffs": "季後賽",
                        "Group Stage": "小組賽",
                        "Swiss Stage": "瑞士輪",
                        "Regular Phase": "例行賽",
                        "Upper Semifinals": "勝部準決賽",
                        "Lower Semifinals": "敗部準決賽",
                        "Grand Final": "總決賽",
                        "Kickoff": "啟動賽",
                        "Pacific": "太平洋賽區",
                        "Americas": "美洲賽區",
                        "EMEA": "歐洲賽區",
                        "China": "中國賽區",
                        "Week": "第",
                        "Round": "第",
                        "Stage": "階段"
                    }
                    for eng, chi in terms.items():
                        text = text.replace(eng, chi)
                    return text

                for match in display_matches:
                    team1 = str(match.get('team1') or 'TBD')
                    team2 = str(match.get('team2') or 'TBD')
                    
                    # 🌟 防彈升級 2：確保翻譯和替換文字時，絕對是字串
                    raw_event = str(match.get('match_event') or '未知賽事')
                    raw_series = str(match.get('match_series') or '')
                    
                    event = translate_terms(raw_event)
                    series = translate_terms(raw_series)
                    event_display = f"{event} - {series}" if series else event
                    
                    raw_time = str(match.get('time_until_match') or '時間未定')
                    time_info = raw_time.replace('from now', '後開打').replace('d', '天').replace('h', '小時').replace('m', '分鐘')
                    
                    embed.add_field(
                        name=f"⚔️ {team1}  vs  {team2}",
                        value=f"🏆 {event_display}\n⏰ {time_info}",
                        inline=False
                    )
                    
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send("❌ 無法取得賽事資料，請稍後再試。")
        except Exception as e:
            print(f"賽事查詢錯誤: {e}")
            await interaction.followup.send("⚠️ 系統擷取電競資料庫時發生錯誤。")


# --- 模組 B：終極按鈕主選單 ---
class ValoMenu(View):
    def __init__(self):
        super().__init__(timeout=None) 

    # 按鈕 1：商店 (藍色)
    @discord.ui.button(label="今日組合包", style=discord.ButtonStyle.blurple, emoji="🛍️")
    async def bundle_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=False)
        try:
            url = "https://api.henrikdev.xyz/valorant/v1/store-featured"
            res = requests.get(url, headers={"Authorization": API_KEY}, timeout=10)
            if res.status_code == 200:
                b_info = res.json()['data'][0] if isinstance(res.json()['data'], list) else res.json()['data']
                items = b_info.get('FeaturedBundle', {}).get('Bundle', {}).get('Items', []) or b_info.get('Bundle', {}).get('Items', [])
                b_id = b_info.get('FeaturedBundle', {}).get('Bundle', {}).get('DataAssetID', '') or b_info.get('Bundle', {}).get('DataAssetID', '')
                
                total = sum(int(i.get('DiscountedPrice', 0)) for i in items)
                b_name, b_img = "未知主打組合包", ""
                
                if b_id:
                    asset_res = requests.get(f"https://valorant-api.com/v1/bundles/{b_id}?language=zh-TW", timeout=10)
                    if asset_res.status_code == 200:
                        b_name = asset_res.json().get('data', {}).get('displayName', b_name)
                        b_img = asset_res.json().get('data', {}).get('displayIcon', '') 
                
                embed = discord.Embed(title=f"✨ 本期主打：【 {b_name} 】", color=0xFF4655)
                embed.add_field(name="💰 總價格", value=f"**{total} VP**")
                if b_img: embed.set_image(url=b_img)
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send("❌ 抓取商店失敗。")
        except Exception:
            await interaction.followup.send("⚠️ 系統錯誤。")

    # 按鈕 2：雷達圖 (紅色)
    @discord.ui.button(label="戰力雷達圖", style=discord.ButtonStyle.red, emoji="🎯")
    async def radar_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(RadarModal())

    # 按鈕 3：歷史戰報 (綠色)
    @discord.ui.button(label="最新戰報", style=discord.ButtonStyle.green, emoji="⚔️")
    async def history_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(HistoryModal())

    # 按鈕 4：牌位查詢 (灰色)
    @discord.ui.button(label="牌位查詢", style=discord.ButtonStyle.gray, emoji="🏆")
    async def rank_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(RankModal())

    # 按鈕 5：電競賽事 (紫色) - 🌟 升級為呼叫彈出式搜尋視窗
    @discord.ui.button(label="近期賽事", style=discord.ButtonStyle.primary, emoji="📺")
    async def esports_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(EsportsModal())

# --- 模組 C：觸發主選單指令 ---
@bot.command()
async def menu(ctx):
    embed = discord.Embed(
        title="🎮 特戰英豪戰術終端機 (All-in-One)",
        description="指揮官，系統已上線。請點擊下方的按鈕選擇您需要的服務：\n\n"
                    "🛍️ **今日組合包**：免輸入，直接讀取今日商店大包\n"
                    "🎯 **戰力雷達圖**：輸入 ID，生成近 5 場戰力六角圖\n"
                    "⚔️ **最新戰報**：輸入 ID，取得上一場對戰詳細 KDA\n"
                    "🏆 **牌位查詢**：輸入 ID，查詢目前階級與系統總分\n"
                    "📺 **近期賽事**：可選填戰隊名稱，追蹤 VCT 賽程與特定戰隊", 
        color=0x2b2d31 
    )
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Valorant_logo_-_pink_color_version.svg/512px-Valorant_logo_-_pink_color_version.svg.png")
    await ctx.send(embed=embed, view=ValoMenu())
bot.run(TOKEN)