import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# Tìm tất cả stats.csv
csv_files = glob.glob("data/results/*/stats.csv")
if not csv_files:
    print("Không tìm thấy stats.csv! Chạy: bash tests/run_batch.sh")
    exit()

data = []
for f in csv_files:
    df = pd.read_csv(f)
    algo = os.path.basename(os.path.dirname(f))
    df['algorithm'] = algo.replace('_compact', '')  # bỏ _compact nếu có
    data.append(df)
df = pd.concat(data).drop_duplicates()

# Chuyen micro s thanh so
def parse_time(t):
    if 'µs' in t:
        return float(t.replace(' µs', '')) / 1_000_000
    elif 'ms' in t:
        return float(t.replace(' ms', '')) / 1000
    else:
        return float(t.replace(' s', ''))

df['alloc_sec'] = df['total_time_alloc'].apply(parse_time)
df['dealloc_sec'] = df['total_time_dealloc'].apply(parse_time)

# Vẽ biểu đồ
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# 1. Thời gian
x = range(len(df))
ax1.bar([i-0.2 for i in x], df['alloc_sec']*1e6, width=0.4, label='Allocation', color='skyblue')
ax1.bar([i+0.2 for i in x], df['dealloc_sec']*1e6, width=0.4, label='Deallocation', color='lightcoral')
ax1.set_xticks(x)
ax1.set_xticklabels(df['algorithm'])
ax1.set_ylabel('Time (µs)')
ax1.set_title('So sánh tốc độ cấp phát & thu hồi')
ax1.legend()
ax1.grid(True, axis='y', alpha=0.3)

# 2. Phân mảnh
ax2.bar(df['algorithm'], df['fragmentation'], color='orange')
ax2.set_ylabel('Fragmentation (%)')
ax2.set_title('So sánh mức độ phân mảnh')
ax2.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('data/results/comparison_chart.png', dpi=150, bbox_inches='tight')
plt.show()

print("Biểu đồ đã lưu: data/results/comparison_chart.png")