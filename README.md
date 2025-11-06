# Memory Allocator Simulator

**Ứng dụng mô phỏng cấp phát bộ nhớ** với **giao diện GUI trực quan**, hỗ trợ **4 thuật toán**, **chạy script tự động**, **xuất ảnh & thống kê**, **so sánh hiệu suất bằng biểu đồ**.

> **Môn học**: Hệ điều hành  
> **Lớp**: SE2039  
> **Ngôn ngữ**: Python 3.8+  
> **GUI**: `tkinter` + `matplotlib` (Tcl/Tk 8.6)  
> **Hệ điều hành**: Windows, Ubuntu, macOS

---

## 🔄 Flow tổng thể (Mermaid)

```mermaid
flowchart TD
  A[Run GUI<br/>python src/gui.py] --> B[gui.py: Create Window]
  B --> C[allocator.py: Init 1024 KB]
  C --> D[visualizer.py: Draw Initial Memory Map]
  D --> E[utils.py: Compute Stats]
  E --> F[gui.py: Update Status Bar]

  subgraph manual [User Actions]
    direction TB
    G[Select Algorithm<br/>Input Size + PID] --> H[Click Allocate/Deallocate/Compact]
    H --> I[algorithms.py: Choose Block]
    I --> J[allocator.py: Update Memory]
    J --> K[visualizer.py: Redraw Memory]
    K --> L[utils.py: Calc Fragmentation]
    L --> M[stats.py: Write CSV]
    M --> F
  end

  subgraph script [Load Script]
    N[Click Load Script] --> O[Select .txt File]
    O --> P[utils.py: read_input_file]
    P --> Q[Iterate Commands]
    Q --> I
  end

  subgraph batch [Auto Test]
    R[bash tests/run_batch.sh] --> S[src/main.py]
    S --> P
    S --> M
    S --> T[data/results/batch_summary.csv]
  end

  subgraph compare [Compare]
    T --> U[python plot_comparison.py]
    U --> V[visualizer.py: Draw Bar Chart]
    V --> W[data/results/comparison_plot.png]
  end

  F --> X[Save Image → PNG/PDF]
  M --> Y[Save Stats → stats.csv]

  F --> G
  F --> N
```

---

## 🖼 GUI Preview

![GUI Preview](img/gui_preview.png)

---

## ✅ Tính năng nổi bật

| Tính năng | Mô tả |
|---------|------|
| **GUI Live View** | Hiển thị bộ nhớ theo thời gian thực |
| **4 thuật toán** | First Fit, Next Fit, Best Fit, Worst Fit |
| **Status Bar** | Fragmentation % với **màu cảnh báo (xanh/cam/đỏ)** |
| **Load Script** | Chạy file `.txt` tự động |
| **Compact Animation** | Hiệu ứng trượt mượt khi nén bộ nhớ |
| **Save Image / Stats** | Xuất PNG, PDF, CSV |
| **So sánh hiệu suất** | `plot_comparison.py` vẽ biểu đồ cột |
| **Test tự động** | `run_batch.sh` chạy tất cả script |

---

## 📁 Cấu trúc thư mục

```
Memory_Allocator/
├── README.md
├── Requirements.txt
├── plot_comparison.py        ← Vẽ biểu đồ so sánh
├── requirements.txt
├── data/
│   └── results/              ← [Tự tạo] PNG, CSV, stats.csv
├── src/
│   ├── algorithms.py         ← Triển khai 4 thuật toán
│   ├── allocator.py          ← Core: quản lý bộ nhớ
│   ├── gui.py                ← Giao diện chính (tkinter + matplotlib)
│   ├── main.py               ← CLI entry (dùng cho batch test)
│   ├── stats.py              ← Ghi thống kê vào CSV
│   ├── utils.py              ← Đọc script, tính fragmentation
│   └── visualizer.py         ← Hỗ trợ vẽ biểu đồ
├── tests/
│   ├── run_batch.sh          ← Chạy tất cả script test
│   └── scripts/
│       ├── compaction_test.txt
│       ├── multitasking.txt
│       ├── producer_consumer.txt
│       ├── sample.txt
│       └── web_server.txt
```

---

## 🔧 Cài đặt

### ✅ Ubuntu

```bash
# Cài tkinter (Tcl/Tk 8.6)
sudo apt update
sudo apt install python3-tk -y

# Tạo môi trường ảo
python3 -m venv venv
source venv/bin/activate

# Cài thư viện
pip install -r requirements.txt

# Chạy GUI
python src/gui.py
```

### ✅ Windows

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src\gui.py
```

> `tkinter` đi kèm Python trên Windows → không cần cài thêm  

---

## ▶️ Chạy chương trình

### ✅ 1) Giao diện GUI
```bash
python src/gui.py
```

### ✅ 2) Chạy tất cả test tự động
```bash
bash tests/run_batch.sh
```

### ✅ 3) Vẽ biểu đồ so sánh hiệu suất
```bash
python plot_comparison.py
```

---

## 📜 Dùng Script Test

### ✅ Cách 1: Trong GUI
- Nhấn **Load Script**
- Chọn file trong `tests/scripts/`

### ✅ Cách 2: Dùng CLI
```bash
python src/main.py --script tests/scripts/web_server.txt --algo best_fit
```

---

## 📄 File script mẫu

`tests/scripts/sample.txt`

```
allocate 200 P1
allocate 300 P2
deallocate P1
allocate 150 P3
compact
allocate 100 P4
show_stats
```

---

## 📂 Kết quả xuất ra

| Hành động | File tạo |
|----------|---------|
| Save Image | `data/results/first_fit_2025...png` |
| Save Stats | `data/results/stats.csv` |
| Batch Test | `data/results/batch_summary.csv` |
| So sánh | `data/results/comparison_plot.png` |

---

## 📊 So sánh hiệu suất

```bash
python plot_comparison.py
```
→ Tạo biểu đồ: **Fragmentation % trung bình theo thuật toán**

---

## 🖥️ Giao diện GUI

> (Ảnh demo)
```
<img src="data/results/gui_preview.png" alt="GUI Preview">
```

> (Tự động lưu khi nhấn "Save Image")

---

## ✅ Không sinh file `.pyc`
- `pyproject.toml` → ngăn tạo `__pycache__`
- `.gitignore` → không commit file rác

---

## 👤 Tác giả

| Thông tin | Nội dung |
|----------|---------|
| Họ tên | *[Tên sinh viên]* |
| MSSV | *[Mã số]* |
| Email | *[email@edu.vn]* |

---

## 📄 License

MIT

