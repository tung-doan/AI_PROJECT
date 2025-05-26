import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from maze.maze import Maze

"""
File này dùng để so sánh thời gian tạo mê cung giữa hai thuật toán DFS Backtracker và Prim
- Tạo mê cung với nhiều kích thước khác nhau
- Đo thời gian thực hiện của mỗi thuật toán
- Vẽ biểu đồ so sánh
- Lưu kết quả vào file CSV
"""

def measure_maze_generation_time(size, algorithm, num_trials=5):
    """
    Đo thời gian trung bình để tạo mê cung với kích thước và thuật toán cho trước
    
    Args:
        size: Kích thước của mê cung
        algorithm: Thuật toán tạo mê cung ("dfs_backtrack" hoặc "prim")
        num_trials: Số lần lặp lại để tính trung bình
        
    Returns:
        Thời gian trung bình (giây)
    """
    total_time = 0
    
    for _ in range(num_trials):
        start_time = time.time()
        
        # Tạo mê cung mà không in ra thông báo
        # Sử dụng một cách tiếp cận khác để tắt đầu ra từ hàm print
        import sys
        from io import StringIO
        
        # Lưu trữ đầu ra tiêu chuẩn
        old_stdout = sys.stdout
        # Chuyển hướng đầu ra đến một bộ đệm
        sys.stdout = StringIO()
        
        # Tạo mê cung
        maze = Maze(size, complexity=0, algorithm=algorithm)
        
        # Khôi phục đầu ra tiêu chuẩn
        sys.stdout = old_stdout
        
        end_time = time.time()
        total_time += (end_time - start_time)
    
    return total_time / num_trials

def compare_algorithms(sizes):
    """
    So sánh thời gian tạo mê cung của hai thuật toán với nhiều kích thước khác nhau
    
    Args:
        sizes: Danh sách các kích thước mê cung cần đo
        
    Returns:
        DataFrame chứa kết quả so sánh
    """
    results = []
    
    for size in sizes:
        print(f"Đang so sánh với kích thước {size}x{size}...")
        
        dfs_time = measure_maze_generation_time(size, "dfs_backtrack")
        prim_time = measure_maze_generation_time(size, "prim")
        
        results.append({
            "Kích thước": size,
            "DFS Backtracker (s)": dfs_time,
            "Prim (s)": prim_time
        })
        
        print(f"  DFS Backtracker: {dfs_time:.4f}s")
        print(f"  Prim: {prim_time:.4f}s")
    
    return pd.DataFrame(results)

def plot_comparison(results):
    """
    Vẽ biểu đồ so sánh thời gian thực hiện
    
    Args:
        results: DataFrame chứa kết quả so sánh
    """
    plt.figure(figsize=(10, 6))
    
    # Vẽ biểu đồ đường
    plt.plot(results["Kích thước"], results["DFS Backtracker (s)"], marker='o', label="DFS Backtracker")
    plt.plot(results["Kích thước"], results["Prim (s)"], marker='x', label="Prim")
    
    plt.title("So sánh thời gian tạo mê cung")
    plt.xlabel("Kích thước mê cung")
    plt.ylabel("Thời gian (giây)")
    plt.legend()
    plt.grid(True)
    
    # Tạo thư mục results nếu chưa tồn tại
    if not os.path.exists("results"):
        os.makedirs("results")
    
    # Lưu biểu đồ đường
    plt.savefig("results/maze_generation_comparison.png")
    
    # Vẽ biểu đồ cột
    plt.figure(figsize=(10, 6))
    
    # Tạo dữ liệu cho biểu đồ cột
    bar_width = 0.35
    x = np.arange(len(results["Kích thước"]))
    
    plt.bar(x - bar_width/2, results["DFS Backtracker (s)"], bar_width, label="DFS Backtracker")
    plt.bar(x + bar_width/2, results["Prim (s)"], bar_width, label="Prim")
    
    plt.title("So sánh thời gian tạo mê cung")
    plt.xlabel("Kích thước mê cung")
    plt.ylabel("Thời gian (giây)")
    plt.xticks(x, results["Kích thước"])
    plt.legend()
    plt.grid(True, axis="y")
    
    # Lưu biểu đồ cột
    plt.savefig("results/maze_generation_bar_chart.png")
    
    # Hiển thị cả hai biểu đồ
    plt.show()

if __name__ == "__main__":
    # Danh sách các kích thước mê cung cần đo
    sizes = [10, 20, 50, 100]
    
    # So sánh thời gian tạo mê cung
    print("\nBắt đầu so sánh thời gian tạo mê cung...")
    results = compare_algorithms(sizes)
    
    # In bảng kết quả
    print("\nKết quả so sánh:")
    print(results)
    
    # Lưu kết quả vào file CSV
    results.to_csv("results/maze_generation_times.csv", index=False)
    print("Đã lưu kết quả vào file results/maze_generation_times.csv")
    
    # Vẽ biểu đồ so sánh
    print("\nĐang vẽ biểu đồ so sánh...")
    plot_comparison(results)
    print("Đã lưu biểu đồ vào thư mục results/")