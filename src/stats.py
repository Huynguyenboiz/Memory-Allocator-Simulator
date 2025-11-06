import csv
import os
from utils import calculate_stats

# Chuyển giây sang chuỗi (micro-giây hoặc giây)
def _format_time(t):
    if t >= 1.0:
        return f"{t:.6f} s"
    elif t >= 0.001:
        return f"{t*1000:.3f} ms"
    else:
        return f"{t*1_000_000:.2f} µs"

def save_stats(allocator, algorithm,
               total_time_alloc=0, total_time_dealloc=0,
               output_dir='data/results', file_name='stats.csv'):
    stats = calculate_stats(allocator)
    stats['algorithm'] = algorithm
    stats['total_time_alloc'] = _format_time(total_time_alloc)
    stats['total_time_dealloc'] = _format_time(total_time_dealloc)

    file_path = os.path.join(output_dir, file_name)
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=stats.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(stats)

    print(f"Saved stats to {file_path}")