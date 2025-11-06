import matplotlib.pyplot as plt
import os
import time

def _short_label(pid, size):
    """Rút gọn nhãn: P1(80)  →  P1(80)  (đủ ngắn)"""
    if pid is None:
        return f"Free ({size})"
    # Nếu PID quá dài → chỉ lấy 6 ký tự đầu
    short_pid = pid[:6] + ("…" if len(pid) > 6 else "")
    return f"{short_pid}({size})"

def visualize_memory(memory_map, algorithm, step, output_dir='data/results'):
    fig, ax = plt.subplots(figsize=(12, 2.2))      # tăng chiều cao một chút
    current_pos = 0
    colors = {'allocated': '#1f77b4', 'free': '#2ca02c'}

    for start, size, status, pid in memory_map:
        # ---- vẽ khối ----
        ax.barh(0, size, left=current_pos,
                color=colors[status], edgecolor='black', linewidth=0.8)

        # ---- quyết định có hiện chữ không ----
        label = _short_label(pid, size)
        # Chỉ hiện nếu khối >= 60 đơn vị hoặc là Free (luôn hiện)
        if status == 'free' or size >= 60:
            # Tính toán vị trí chữ
            text_x = current_pos + size / 2
            # Font size tự động giảm khi khối nhỏ
            font_size = max(8, min(12, size // 8))
            ax.text(text_x, 0, label,
                    ha='center', va='center',
                    color='white', fontsize=font_size,
                    fontweight='bold',
                    rotation=0)

        current_pos += size

    # ---- trục ----
    ax.set_ylim(-0.8, 0.8)
    ax.set_xlim(0, current_pos)
    ax.axis('off')
    ax.set_title(f"{algorithm.replace('_', ' ').title()} – Step {step}",
                 fontsize=14, pad=20)

    # ---- lưu file ----
    os.makedirs(output_dir, exist_ok=True)
    timestamp = int(time.time())
    file_path = os.path.join(output_dir,
                f"{algorithm}_step_{step}_{timestamp}.png")
    plt.savefig(file_path, dpi=150, bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print(f"Saved visualization: {file_path}")
    return fig
