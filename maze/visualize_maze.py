import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def visualize_maze(maze_obj):
    """
    Visualize a maze with filled walls
    maze_obj: instance of Maze class
    """
    maze = maze_obj.get_maze()
    size = maze_obj.size
    
    # Tạo hình vẽ
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Duyệt qua tất cả các ô trong mê cung
    for i in range(size):
        for j in range(size):
            if maze[i, j] == 1:  # Nếu là tường
                # Tạo hình chữ nhật tô đặc
                rect = Rectangle((j, i), 1, 1, facecolor='navy', edgecolor='navy')
                ax.add_patch(rect)
    
    # Thiết lập giới hạn trục
    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    
    # Ẩn các trục
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Đảo ngược trục y để phù hợp với hiển thị mê cung
    ax.invert_yaxis()
    
    # Thiết lập tỷ lệ bằng nhau trên cả hai trục
    ax.set_aspect('equal')
    
    # Đánh dấu điểm bắt đầu và kết thúc
    start = maze_obj.start
    end = maze_obj.end
    ax.plot(start[1] + 0.5, start[0] + 0.5, 'go', markersize=8)
    ax.plot(end[1] + 0.5, end[0] + 0.5, 'ro', markersize=8)
    
    # Đặt màu nền trắng
    ax.set_facecolor('white')
    
    plt.title('Maze Visualization')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Example usage
    from maze import Maze
    maze_obj = Maze(size=300, complexity=0.1)
    from algorithm.a_star_midterm import find_path_and_visualize as a_star_find_path_and_visualize
    a_star_find_path_and_visualize(maze_obj)