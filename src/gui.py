import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from allocator import Allocator
from utils import calculate_stats, read_input_file  # Đảm bảo có read_input_file
from stats import save_stats
import os
import time

class MemoryGUI:
    def __init__(self, total_memory=1024):
        # === 1. TẠO CỬA SỔ CHÍNH ===
        self.root = tk.Tk()
        self.root.title("Memory Allocator Simulator")
        self.root.geometry("1200x700")
        self.root.minsize(800, 500)

        # === 2. TẠO BIẾN TKINTER ===
        self.algorithm = tk.StringVar(self.root, value='first_fit')
        self.size_var = tk.StringVar(self.root)
        self.pid_var = tk.StringVar(self.root)
        self.status_var = tk.StringVar(self.root, value="Ready")  # Status bar text

        # === 3. KHỞI TẠO ALLOCATOR ===
        self.allocator = Allocator(total_memory)

        # === 4. CẤU HÌNH STYLE CHO NÚT ===
        style = ttk.Style()
        style.configure('Big.TButton',
                        font=('Helvetica', 10, 'bold'),
                        padding=(10, 8))

        # === 5. LAYOUT CHÍNH ===
        self.paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Control Panel ---
        control_frame = ttk.LabelFrame(self.paned, text=" Control Panel ", padding=20)
        control_frame.pack_propagate(False)
        self.paned.add(control_frame, weight=1)

        # Responsive grid
        for i in range(11):  # +1 cho Load Script
            control_frame.grid_rowconfigure(i, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)

        # Algorithm
        ttk.Label(control_frame, text="Algorithm:", font=('Helvetica', 11, 'bold')).grid(row=0, column=0, sticky='w', pady=8)
        ttk.Combobox(control_frame, textvariable=self.algorithm,
                     values=['first_fit', 'next_fit', 'best_fit', 'worst_fit'],
                     state='readonly', font=('Helvetica', 10)).grid(row=0, column=1, sticky='ew', padx=10, pady=8)

        # Size
        ttk.Label(control_frame, text="Size (KB):", font=('Helvetica', 10)).grid(row=1, column=0, sticky='w', pady=8)
        ttk.Entry(control_frame, textvariable=self.size_var, width=15, font=('Helvetica', 10)).grid(row=1, column=1, sticky='ew', padx=10, pady=8)

        # PID
        ttk.Label(control_frame, text="PID:", font=('Helvetica', 10)).grid(row=2, column=0, sticky='w', pady=8)
        ttk.Entry(control_frame, textvariable=self.pid_var, width=15, font=('Helvetica', 10)).grid(row=2, column=1, sticky='ew', padx=10, pady=8)

        # Buttons
        ttk.Button(control_frame, text="Allocate", command=self.allocate, style='Big.TButton').grid(row=3, column=0, columnspan=2, pady=10, sticky='ew')
        ttk.Button(control_frame, text="Deallocate", command=self.deallocate, style='Big.TButton').grid(row=4, column=0, columnspan=2, pady=10, sticky='ew')
        ttk.Button(control_frame, text="Compact", command=self.compact, style='Big.TButton').grid(row=5, column=0, columnspan=2, pady=10, sticky='ew')
        ttk.Button(control_frame, text="Load Script", command=self.load_script, style='Big.TButton').grid(row=6, column=0, columnspan=2, pady=10, sticky='ew')  # MỚI
        ttk.Button(control_frame, text="Show Stats", command=self.show_stats, style='Big.TButton').grid(row=7, column=0, columnspan=2, pady=10, sticky='ew')
        ttk.Button(control_frame, text="Save Stats", command=self.save_current_stats, style='Big.TButton').grid(row=8, column=0, columnspan=2, pady=10, sticky='ew')
        ttk.Button(control_frame, text="Save Image", command=self.save_image, style='Big.TButton').grid(row=9, column=0, columnspan=2, pady=15, sticky='ew')

        # --- Canvas ---
        self.fig, self.ax = plt.subplots(figsize=(10, 2.5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.paned)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.paned.add(self.canvas.get_tk_widget(), weight=3)

        # === THANH TRẠNG THÁI (STATUS BAR) ===
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
        ttk.Label(status_frame, text="Status:", font=('Helvetica', 9, 'bold')).pack(side=tk.LEFT)
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, font=('Helvetica', 9), foreground='blue')
        self.status_label.pack(side=tk.LEFT, padx=5)

        # === TỰ ĐỘNG CO GIÃN ===
        self.root.bind("<Configure>", self.on_resize)
        self.last_width = 0
        self.last_height = 0

        # === CẬP NHẬT BAN ĐẦU ===
        self.update_visual()
        self.update_status()  # Cập nhật fragmentation ngay từ đầu
        self.root.mainloop()

    # === CÁC HÀM XỬ LÝ ===
    def allocate(self):
        try:
            size = int(self.size_var.get())
            pid = self.pid_var.get().strip()
            if not pid:
                raise ValueError("PID cannot be empty")
            if size <= 0:
                raise ValueError("Size must be > 0")
            self.allocator.allocate(size, pid, self.algorithm.get())
            self.update_visual()
            self.update_status()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def deallocate(self):
        pid = self.pid_var.get().strip()
        if not pid:
            messagebox.showerror("Error", "Enter PID to deallocate")
            return
        success, _ = self.allocator.deallocate(pid)
        if success:
            messagebox.showinfo("Success", f"Deallocated {pid}")
        else:
            messagebox.showwarning("Not Found", f"Process {pid} not found")
        self.update_visual()
        self.update_status()

    def compact(self):
        self.allocator.compact()
        self.update_visual()
        self.update_status()
        messagebox.showinfo("Compaction", "Memory compacted!")

    def show_stats(self):
        stats = calculate_stats(self.allocator)
        msg = (f"Total Free: {stats['total_free']} KB\n"
               f"Total Allocated: {stats['total_allocated']} KB\n"
               f"Fragmentation: {stats['fragmentation']:.2f}%\n")
        messagebox.showinfo("Memory Stats", msg)

    def save_current_stats(self):
        save_stats(self.allocator, self.algorithm.get())
        messagebox.showinfo("Saved", "Stats saved to data/results/stats.csv")

    def save_image(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("PDF File", "*.pdf")],
            title="Save Memory Map"
        )
        if file_path:
            self.fig.savefig(file_path, dpi=150, bbox_inches='tight', pad_inches=0.3)
            messagebox.showinfo("Saved", f"Image saved:\n{file_path}")

    # === TÍNH NĂNG MỚI: LOAD SCRIPT ===
    def load_script(self):
        file_path = filedialog.askopenfilename(
            title="Select Script File",
            filetypes=[("Text Files", "*.txt")],
            initialdir="tests/scripts"  # Đảm bảo thư mục tồn tại
        )
        if not file_path:
            return
        try:
            commands = read_input_file(file_path)
            self.status_var.set(f"Running {os.path.basename(file_path)}...")
            self.root.update()
            for cmd in commands:
                if cmd[0] == 'allocate':
                    self.allocator.allocate(cmd[1], cmd[2], self.algorithm.get())
                elif cmd[0] == 'deallocate':
                    self.allocator.deallocate(cmd[1])
                elif cmd[0] == 'compact':
                    self.allocator.compact()
                self.update_visual()
                self.update_status()
                self.root.update_idletasks()
                time.sleep(0.1)  # Delay nhẹ để thấy hiệu ứng
            self.status_var.set("Script executed!")
            messagebox.showinfo("Success", f"Script {os.path.basename(file_path)} executed!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run script:\n{e}")

    # === CẬP NHẬT THANH TRẠNG THÁI ===
    def update_status(self):
        stats = calculate_stats(self.allocator)
        frag = stats['fragmentation']
        # Đổi màu theo mức độ phân mảnh
        if frag < 20:
            color = 'green'
        elif frag < 50:
            color = 'orange'
        else:
            color = 'red'
        self.status_var.set(f"Fragmentation: {frag:.2f}%")
        self.status_label.config(foreground=color)

    # === TỰ ĐỘNG CO GIÃN ===
    def on_resize(self, event):
        if event.widget != self.root:
            return
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        if abs(width - self.last_width) < 20 and abs(height - self.last_height) < 20:
            return
        self.last_width = width
        self.last_height = height
        self.root.after(100, self.update_visual)

    # === CẬP NHẬT HÌNH ẢNH ===
    def update_visual(self):
        self.ax.clear()
        memory_map = self.allocator.get_memory_map()
        current_pos = 0
        colors = {'allocated': '#1f77b4', 'free': '#2ca02c'}

        for start, size, status, pid in memory_map:
            if status == 'allocated':
                if size < 100:
                    short_pid = pid[:5] + "..." if len(pid) > 5 else pid
                    label = f"{short_pid} ({size})"
                else:
                    label = f"{pid} ({size})"
                text_color = 'white'
            else:
                label = f"Free ({size})"
                text_color = 'white'

            self.ax.barh(0, size, left=current_pos, color=colors[status], edgecolor='black', linewidth=0.9)

            if size >= 50:
                self.ax.text(
                    current_pos + size / 2, 0, label,
                    ha='center', va='center',
                    color=text_color,
                    fontsize=9,
                    fontweight='bold',
                    clip_on=True
                )

            current_pos += size

        self.ax.set_ylim(-1, 1)
        self.ax.set_xlim(0, max(current_pos, 1))
        self.ax.axis('off')
        self.ax.set_title(f"{self.algorithm.get().replace('_', ' ').title()} - Live View", fontsize=13, pad=20)

        canvas_width = self.canvas.get_tk_widget().winfo_width() / 100
        canvas_height = self.canvas.get_tk_widget().winfo_height() / 100
        if canvas_width > 5 and canvas_height > 1:
            self.fig.set_size_inches(canvas_width * 0.9, canvas_height * 0.7)

        self.canvas.draw()

# === CHẠY CHƯƠNG TRÌNH ===
if __name__ == "__main__":
    MemoryGUI()