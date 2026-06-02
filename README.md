\# 🎮 特戰英豪戰術終端機 (Valorant Tactical Terminal)



!\[Python](https://img.shields.io/badge/Python-3.8%2B-blue)

!\[Discord.py](https://img.shields.io/badge/Discord.py-2.0%2B-blueviolet)

!\[Matplotlib](https://img.shields.io/badge/Matplotlib-Data\_Visualization-green)

!\[Status](https://img.shields.io/badge/Status-Active-brightgreen)



這是一個專為《特戰英豪》(Valorant) 玩家社群打造的 All-in-One Discord 互動式機器人。

有別於傳統的指令型機器人，本專案採用 Discord UI Modal 與 Button 建立全圖形化操作介面，並串接第三方 RESTful API，實現遊戲數據視覺化、戰績查詢與電競賽事追蹤等微服務。



\## ✨ 核心功能 (Features)



本系統提供五大核心模組，玩家只需透過點擊按鈕即可呼叫對應功能：



1\. 🛍️ \*\*今日組合包 (Store Fetcher)\*\*

&#x20;  - 繞過登入風險，透過公開 API 即時解析官方商店資料。

&#x20;  - 抓取當期主打武器造型、計算總 VP 價格，並動態生成預覽縮圖。



2\. 🎯 \*\*戰力雷達圖 (Stats Radar Visualization)\*\*

&#x20;  - 導入 `Matplotlib` 與中文字型渲染技術。

&#x20;  - 撈取玩家近 5 場賽事數據，自動運算 KDA、爆頭率與綜合表現，並於記憶體中動態繪製「戰力六角雷達圖」，直觀呈現玩家近期狀態。



3\. ⚔️ \*\*最新戰報 (Recent Match)\*\*

&#x20;  - 輸入 Riot ID 即可快速調閱上一場對戰詳細資訊。

&#x20;  - 包含對戰地圖、使用特工、KDA 數據，並自動換算 KDA 評分。



4\. 🏆 \*\*牌位與隱分查詢 (Rank \& MMR Checker)\*\*

&#x20;  - 即時連線 Riot 伺服器，精準抓取玩家目前階級。

&#x20;  - 顯示競技積分 (RR) 與系統隱藏總積分 (Elo)。



5\. 📺 \*\*賽事導航中心 (Esports Hub - 容錯降級版)\*\*

&#x20;  - 針對大型國際賽事（如 VCT 大師賽、冠軍賽）提供零延遲的導航面板。

&#x20;  - 具備 `ephemeral` 隱私保護機制，點擊後僅使用者可見，避免洗版群組。整合官方中文直播與 VLR.gg/Liquipedia 賽程數據庫。



\## 🛠️ 技術棧 (Tech Stack)



\* \*\*後端框架：\*\* Python 3, `discord.py`

\* \*\*資料視覺化：\*\* `matplotlib` (Polar 座標系繪圖)

\* \*\*API 串接：\*\* `requests`, `urllib` (處理 JSON 解析與字串 URL 編碼)

\* \*\*環境變數管理：\*\* `python-dotenv`

\* \*\*雲端部署：\*\* Render (支援 24/7 待機運行與自動建置)



\## 💡 工程亮點 (Engineering Highlights)



\* \*\*互動式 UI 介面：\*\* 全面棄用傳統 `!指令`，改用 `discord.ui` 的 Button 與 Modal，大幅降低使用者操作門檻。

\* \*\*資料防呆與容錯處理：\*\* - 處理 API 回傳的 Null/None 異常值（強制轉型防護）。

&#x20; - 實作超時 (Timeout) 捕捉與例外處理 (Exception Handling)。

&#x20; - 在第三方 API 伺服器阻擋爬蟲時，採用\*\*「降級策略 (Graceful Degradation)」\*\*，將動態查詢轉換為高穩定性的靜態導航面板，確保使用者體驗不中斷。



\## 🚀 部署與執行 (Getting Started)



1\. \*\*Clone 專案：\*\*

&#x20;  ```bash

&#x20;  git clone \[https://github.com/YourUsername/Valorant-Tactical-Terminal.git](https://github.com/YourUsername/Valorant-Tactical-Terminal.git)

