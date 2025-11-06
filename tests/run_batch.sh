#!/bin/bash

# Kiểm tra thư mục gốc
if [ ! -d "src" ] || [ ! -d "tests" ]; then
    echo "ERROR: Please run this script from the project root (Memory_Allocator/)"
    echo "Current dir: $(pwd)"
    exit 1
fi

algorithms=("first_fit" "next_fit" "best_fit" "worst_fit")

# Test cases
test_cases=("sample.txt" "compaction_test.txt" "web_server.txt" "producer_consumer.txt" "multitasking.txt")

for algo in "${algorithms[@]}"; do
    for tc in "${test_cases[@]}"; do
        echo "Running Python $algo with $tc..."
        python3 src/main.py --algorithm $algo --input tests/scripts/$tc --output data/results/${algo}_${tc} --compact_threshold 30 || echo "Failed: $algo $tc"
    done
done

echo "All done! Results in data/results/"
echo "To run GUI: python3 src/gui.py"
echo "To plot comparison: python3 plot_comparison.py"

# # Xóa pycache trước khi chạy
# find . -type d -name "__pycache__" -exec rm -rf {} +
# find . -name "*.pyc" -delete

# echo "Đã dọn dẹp .pyc files"
# python src/gui.py