import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 数据（根据合并后的表格）
data = {
    'Sequence': ['Balboa', 'BranCastle', 'Broadway', 'ChairliftRide', 'GasLamp', 'Landing', 'Trolley'],
    'SDAMC_Bitrate': [10309.44, 20289.00, 11230.80, 4487.46, 4003.50, 6636.12, 12091.68],
    'Origin_Bitrate': [10305.84, 20245.74, 11201.76, 4475.28, 4003.56, 6569.28, 12090.06],
    'SDAMC_Y_PSNR': [37.0703, 30.6001, 36.5604, 36.3412, 37.5263, 34.9836, 33.5854],
    'Origin_Y_PSNR': [37.1265, 30.6530, 36.6102, 36.3846, 37.5272, 35.1195, 33.5846],
    'SDAMC_YUV_PSNR': [38.5408, 31.9801, 38.0014, 37.8209, 38.9875, 36.4032, 35.2128],
    'Origin_YUV_PSNR': [38.6033, 32.0393, 38.0555, 37.8653, 38.9884, 36.5482, 35.2120]
}
df = pd.DataFrame(data)

# 设置图形
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
x = np.arange(len(df['Sequence']))          # 序列位置
width = 0.35                                # 柱宽

# ---- 子图1：码率对比 ----
ax1 = axes[0]
bars1 = ax1.bar(x - width/2, df['SDAMC_Bitrate'], width, label='SDAMC', color='#1f77b4')
bars2 = ax1.bar(x + width/2, df['Origin_Bitrate'], width, label='Origin', color='#ff7f0e')
ax1.set_ylabel('Bitrate (kbps)')
ax1.set_title('Bitrate Comparison')
ax1.set_xticks(x)
ax1.set_xticklabels(df['Sequence'], rotation=45, ha='right')
ax1.legend()
# 标注差值（Δ码率）
for i, (sdamc, origin) in enumerate(zip(df['SDAMC_Bitrate'], df['Origin_Bitrate'])):
    delta = sdamc - origin
    color = 'red' if delta > 0 else 'green'
    ax1.annotate(f'{delta:+.1f}', (i, max(sdamc, origin) + 50), ha='center', fontsize=8, color=color)

# ---- 子图2：Y‑PSNR对比 ----
ax2 = axes[1]
ax2.bar(x - width/2, df['SDAMC_Y_PSNR'], width, label='SDAMC', color='#1f77b4')
ax2.bar(x + width/2, df['Origin_Y_PSNR'], width, label='Origin', color='#ff7f0e')
ax2.set_ylabel('Y-PSNR (dB)')
ax2.set_title('Y-PSNR Comparison')
ax2.set_xticks(x)
ax2.set_xticklabels(df['Sequence'], rotation=45, ha='right')
ax2.legend()
for i, (sdamc, origin) in enumerate(zip(df['SDAMC_Y_PSNR'], df['Origin_Y_PSNR'])):
    delta = sdamc - origin
    color = 'red' if delta < 0 else 'green'   # PSNR 降低为负向变化
    ax2.annotate(f'{delta:+.4f}', (i, min(sdamc, origin) - 0.2), ha='center', fontsize=8, color=color)

# ---- 子图3：YUV‑PSNR对比 ----
ax3 = axes[2]
ax3.bar(x - width/2, df['SDAMC_YUV_PSNR'], width, label='SDAMC', color='#1f77b4')
ax3.bar(x + width/2, df['Origin_YUV_PSNR'], width, label='Origin', color='#ff7f0e')
ax3.set_ylabel('YUV-PSNR (dB)')
ax3.set_title('YUV-PSNR Comparison')
ax3.set_xticks(x)
ax3.set_xticklabels(df['Sequence'], rotation=45, ha='right')
ax3.legend()
for i, (sdamc, origin) in enumerate(zip(df['SDAMC_YUV_PSNR'], df['Origin_YUV_PSNR'])):
    delta = sdamc - origin
    color = 'red' if delta < 0 else 'green'
    ax3.annotate(f'{delta:+.4f}', (i, min(sdamc, origin) - 0.2), ha='center', fontsize=8, color=color)

plt.tight_layout()
plt.show()