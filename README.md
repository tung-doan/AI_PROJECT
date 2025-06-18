# Maze Algorithm Visualization

Dự án này là một ứng dụng trực quan hóa các thuật toán tạo mê cung và tìm đường đi bằng Python. Ứng dụng cung cấp giao diện đồ họa thân thiện, tích hợp các thuật toán phổ biến và tạo animation minh họa chi tiết từng bước.

---

## Tính năng

### Thuật toán tạo mê cung

- **DFS Backtracker:** Tạo mê cung sử dụng thuật toán Depth-First Search + Backtracking
- **Prim:** Tạo mê cung dựa trên thuật toán Prim's Minimum Spanning Tree
- **Kruskal:** Tạo mê cung dựa trên thuật toán Kruskal's Minimum Spanning Tree
- **Recursive Division:** Tạo mê cung bằng phương pháp phân chia đệ quy

### Thuật toán tìm đường

- **BFS (Breadth-First Search):** Đảm bảo tìm được đường đi ngắn nhất
- **DFS (Depth-First Search):** Tiết kiệm bộ nhớ, phù hợp cho mê cung phức tạp
- **A (A-Star)\***: Kết hợp ưu điểm của BFS và thuật toán heuristic, tối ưu hóa quá trình tìm kiếm

### Trực quan hóa

- Animation chi tiết từng bước của quá trình tạo mê cung
- Animation từng bước của quá trình tìm đường (đã thăm, đang xét, hàng đợi/stack, đường đi)
- Điều chỉnh tốc độ animation
- Tùy chỉnh kích thước và độ phức tạp của mê cung

---

## Cài đặt

### Yêu cầu hệ thống

- Python 3.6+
- Các thư viện: `numpy`, `matplotlib`, `tkinter`

### Cài đặt các thư viện

```bash
pip install numpy matplotlib
```

**Lưu ý:** Tkinter thường được cài sẵn với Python. Nếu chưa có, hãy cài đặt theo hướng dẫn cho hệ điều hành của bạn.

---

## Cách sử dụng

### Khởi chạy ứng dụng

```bash
python app.py
```

### Giao diện người dùng

- Chọn thuật toán tìm đường (BFS, DFS, hoặc A*)
- Thiết lập kích thước mê cung (10-100)
- Điều chỉnh tốc độ hoạt hình (10-200ms)
- Chọn thuật toán tạo mê cung (Prim, DFS Backtrack, hoặc Kruskal)
- Chọn độ phức tạp (Đơn giản - Chuyên Gia)
- Nhấn nút "Tạo & Trực Quan Hóa" để bắt đầu

---

## Cấu trúc thư mục

```
AI_project/
├── app.py                     # Ứng dụng chính với giao diện đồ họa 
├── animation_create_maze.py   # Tạo animation nâng cao cho quá trình sinh mê cung
├── compare_maze_generation.py # So sánh hiệu suất các thuật toán tạo mê cung
├── algorithm/                 # Các thuật toán tìm đường
│   ├── a_star_final.py        # Thuật toán A*
│   ├── dfs_final.py           # Thuật toán DFS 
│   └── bfs_final.py           # Thuật toán BFS
├── animation/                 # Module animation tìm đường
│   ├── A_STAR_animation.py    # Animation A*
│   ├── bfs_animation.py       # Animation BFS
│   └── dfs_animation.py       # Animation DFS
└── maze/                      # Module tạo và quản lý mê cung
    ├── maze.py                # Lớp Maze chính và các thuật toán tạo mê cung
    ├── dfsmaze_generation_animation.py   # Animation tạo mê cung DFS
    ├── kruskalmaze_generation_animation.py # Animation tạo mê cung Kruskal
    ├── primmaze_generation_animation.py  # Animation tạo mê cung Prim
    └── recursivemaze_generation_animation.py # Animation tạo mê cung Recursive Division 
```

---

## Các chế độ chạy riêng

### Trực quan hóa từng thuật toán riêng biệt

```bash
# Thuật toán A*
python animation/A_STAR_animation.py

# Thuật toán BFS
python animation/bfs_animation.py

# Thuật toán DFS
python animation/dfs_animation.py 
```

### Trực quan hóa quá trình tạo mê cung

```bash
# Animation tạo mê cung DFS Backtracker
python maze/dfsmaze_generation_animation.py

# Animation tạo mê cung Kruskal
python maze/kruskalmaze_generation_animation.py

# Animation tạo mê cung Prim
python maze/primmaze_generation_animation.py

# Animation tạo mê cung Recursive Division
python maze/recursivemaze_generation_animation.py 
```

---

## Đánh giá các thuật toán

### Tạo mê cung:

- **DFS Backtracker:** Tạo mê cung có nhiều đường dài và ít nhánh
- **Prim:** Tạo mê cung có nhiều nhánh ngắn, cân bằng hơn
- **Kruskal:** Tạo mê cung khá ngẫu nhiên, cân bằng giữa nhánh dài và ngắn
- **Recursive Division:** Tạo mê cung có cấu trúc hình học đặc trưng, dễ nhận biết

### Tìm đường:

- **BFS** luôn tìm ra đường đi ngắn nhất nhưng tốn nhiều bộ nhớ
- **A\*** thường có hiệu suất tốt nhất về số bước tìm kiếm
- **DFS** tốn ít bộ nhớ hơn nhưng không đảm bảo đường đi ngắn nhất 

---
