# 🎮 特戰英豪戰術終端機 (Valorant Tactical Terminal)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0%2B-blueviolet)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Data_Visualization-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

這是一個專為《特戰英豪》(Valorant) 玩家社群打造的 All-in-One Discord 互動式機器人。

有別於傳統的指令型機器人，本專案採用 Discord UI Modal 與 Button 建立全圖形化操作介面，並串接第三方 RESTful API，實現遊戲數據視覺化、戰績查詢與電競賽事追蹤等微服務。

## ✨ 核心功能 (Features)

本系統提供五大核心模組，玩家只需透過點擊按鈕即可呼叫對應功能：

1. 🛍️ **今日組合包 (Store Fetcher)**
   - 繞過登入風險，透過公開 API 即時解析官方商店資料。
   - 抓取當期主打武器造型、計算總 VP 價格，並動態生成預覽縮圖。

2. 🎯 **戰力雷達圖 (Stats Radar Visualization)**
   - 導入 Matplotlib 與中文字型渲染技術。
   - 撈取玩家近 5 場賽事數據，自動運算 KDA、爆頭率與綜合表現，並於記憶體中動態繪製「戰力六角雷達圖」，直觀呈現玩家近期狀態。

3. ⚔️ **最新戰報 (Recent Match)**
   - 輸入 Riot ID 即可快速調閱上一場對戰詳細資訊。
   - 包含對戰地圖、使用特工、KDA 數據，並自動換算 KDA 評分。

4. 🏆 **牌位與隱分查詢 (Rank & MMR Checker)**
   - 即時連線 Riot 伺服器，精準抓取玩家目前階級。
   - 顯示競技積分 (RR) 與系統隱藏總積分 (Elo)。

5. 📺 **賽事導航中心 (Esports Hub - 容錯降級版)**
   - 針對大型國際賽事（如 VCT 大師賽、冠軍賽）提供零延遲的導航面板。
   - 具備 ephemeral 隱私保護機制，點擊後僅使用者可見，避免洗版群組。整合官方中文直播與 VLR.gg/Liquipedia 賽程數據庫。

## 🛠️ 技術棧 (Tech Stack)

* 後端框架： Python 3, discord.py
* 資料視覺化： matplotlib (Polar 座標系繪圖)
* API 串接： requests, urllib (處理 JSON 解析與字串 URL 編碼)
* 環境變數管理： python-dotenv
* 雲端部署： Render (支援 24/7 待機運行與自動建置)

## 💡 工程亮點 (Engineering Highlights)

* 互動式 UI 介面： 全面棄用傳統 !指令，改用 discord.ui 的 Button 與 Modal，大幅降低使用者操作門檻。
* 資料防呆與容錯處理：
  - 處理 API 回傳的 Null/None 異常值（強制轉型防護）。
  - 實作超時 (Timeout) 捕捉與例外處理 (Exception Handling)。
  - 在第三方 API 伺服器阻擋爬蟲時，採用「降級策略 (Graceful Degradation)」，將動態查詢轉換為高穩定性的靜態導航面板，確保使用者體驗不中斷。
* 敏感資訊保護： 使用 python-dotenv 讀取環境變數，Token 與 API Key 皆不寫死於程式碼中，避免金鑰外洩風險。

## 🚀 部署與執行 (Getting Started)

1. Clone 專案：

```bash
git clone https://github.com/chenhanhgv/valorant-bot.git
cd valorant-bot
```

2. 安裝依賴套件：

pip install -r requirements.txt

3. 設定環境變數：

在專案根目錄建立 .env 檔案，內容如下：

```
DISCORD_TOKEN=你的Discord Bot Token
VALORANT_API_KEY=你的HenrikDev API Key
```

4. 執行機器人：

python val_bot.py

## 📂 專案結構

```
valorant-bot/
├── val_bot.py          # 主程式：機器人核心邏輯與所有功能模組
├── draw_radar.py        # 雷達圖繪製輔助模組
├── draw_practice.py     # 圖表繪製練習
├── requirements.txt      # 專案依賴套件清單
└── .gitignore            # Git 忽略清單（保護 .env 等敏感檔案）
```

## 📌 未來規劃 (Roadmap)

- [ ] 加入單元測試（Pytest）驗證 API 資料解析邏輯
- [ ] 支援多語言介面切換
- [ ] 新增戰績歷史趨勢圖表
