# ==========================================
# 進階繪圖：特戰英豪玩家能力雷達圖 (全中文版)
# ==========================================

import matplotlib.pyplot as plt
import math

# ⚠️ 關鍵魔法：強制載入 Windows 內建的微軟正黑體，解決中文變方塊的問題
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
# 順手解決有時候數字前面的負號 (-) 會變方塊的問題
plt.rcParams['axes.unicode_minus'] = False

# 1. 準備「能力維度」與「假數據」 (全部換成中文啦！)
categories = ['擊殺能力', '團隊助攻', '爆頭準確率', '經濟控管', '突破首殺']
values = [85, 60, 90, 70, 80] 

# 2. 計算極座標角度
N = len(categories)
angles = [n / float(N) * 2 * math.pi for n in range(N)]
angles += angles[:1]
values += values[:1]

# 3. 建立極座標畫布
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

# 4. 繪製多邊形與填色 (特戰紅)
ax.plot(angles, values, color='#FF4655', linewidth=2, linestyle='solid')
ax.fill(angles, values, color='#FF4655', alpha=0.4)

# 5. 裝飾圖表
# 這裡把刻度換成我們的中文維度名稱
plt.xticks(angles[:-1], categories, fontsize=12, color='black')
ax.set_yticklabels([])

# 設定中文大標題
plt.title("玩家綜合能力分析", size=18, weight='bold', color='#333333', y=1.1)# 6. 生成高畫質圖片
plt.savefig('radar_chart_zh.png', bbox_inches='tight')

print("✅ 中文版雷達圖生成成功！請檢查 'radar_chart_zh.png' 檔案。")