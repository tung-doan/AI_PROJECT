import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maze import Maze

def animate_prim_maze(size=15, interval=100):
    maze_obj = Maze(size, algorithm="prim")
    height, width = maze_obj.maze.shape
    maze = np.ones((height, width), dtype=int) * 4  # Giá trị 4 cho tường
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Tùy chỉnh màu sắc
    colors = {
        4: 'black',    # Tường
        0: 'white',    # Đường đi
        1: 'green',    # Ô đã thăm
        2: 'yellow',   # Ô hiện tại
        3: 'red'       # Ô hàng xóm
    }
    cmap = plt.cm.colors.ListedColormap([colors[0], colors[1], colors[2], colors[3], colors[4]])
    norm = plt.Normalize(0, 4)
    im = ax.imshow(maze, cmap=cmap, norm=norm)

    ax.set_title("Prim's Maze Generation")
    ax.axis('off')

    # Vẽ lưới
    for i in range(height + 1):
        ax.axhline(i - 0.5, color='black', linewidth=1, zorder=10)
    for j in range(width + 1):
        ax.axvline(j - 0.5, color='black', linewidth=1, zorder=10)

    # Chú thích
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color=colors[4], lw=4, label='Wall'),
        Line2D([0], [0], color=colors[0], lw=4, label='Path'),
        Line2D([0], [0], color=colors[1], lw=4, label='Visited Cell'),
        Line2D([0], [0], color=colors[2], lw=4, label='Current Cell'),
        Line2D([0], [0], color=colors[3], lw=4, label='Neighbor Cell')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=8)

    steps = maze_obj.generation_path
    visited_cells = set()
    current_cell = None

    def update(frame):
        nonlocal current_cell, visited_cells
        if frame == 0:
            maze[:, :] = 4  # Toàn bộ là tường
        else:
            step = steps[frame - 1]
            if step[0] == "start_cell":
                maze[step[1], step[2]] = 2  # Ô bắt đầu (current)
                current_cell = (step[1], step[2])
                visited_cells.add(current_cell)
            elif step[0] == "wall_candidate":
                # Không làm gì ở đây vì các ô hàng xóm sẽ được xử lý trong bước "neighbors"
                pass
            elif step[0] == "neighbors":
                # Đặt lại các ô hàng xóm trước đó thành trạng thái phù hợp
                for x, y in [(i, j) for i in range(height) for j in range(width) if maze[i, j] == 3]:
                    if (x, y) in visited_cells:
                        maze[x, y] = 1  # Ô đã thăm
                    else:
                        maze[x, y] = 4  # Tường
                # Đánh dấu các ô hàng xóm mới
                for x, y in step[1]:
                    if (x, y) not in visited_cells:
                        maze[x, y] = 3  # Ô hàng xóm
            elif step[0] == "break_wall":
                maze[step[1], step[2]] = 0  # Phá tường
            elif step[0] == "new_cell":
                if current_cell:
                    maze[current_cell[0], current_cell[1]] = 1  # Ô hiện tại trước đó thành đã thăm
                maze[step[1], step[2]] = 2  # Ô mới là ô hiện tại
                current_cell = (step[1], step[2])
                visited_cells.add(current_cell)
            elif step[0] == "extra_wall":
                maze[step[1], step[2]] = 0  # Đường đi bổ sung

        im.set_array(maze)
        return [im]

    ani = animation.FuncAnimation(
        fig, update, frames=len(steps) + 1, interval=interval, blit=False, repeat=False
    )
    plt.show()

if __name__ == "__main__":
    size = 10      # Kích thước mê cung cố định
    speed = 10     # Tốc độ animation cố định (ms)
    animate_prim_maze(size=size, interval=speed)