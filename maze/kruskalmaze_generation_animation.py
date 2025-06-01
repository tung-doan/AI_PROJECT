import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maze import Maze

def animate_kruskal_maze(size=15, interval=100, save_animation=False):
    maze_obj = Maze(size, algorithm="kruskal")
    height, width = maze_obj.maze.shape
    maze = np.ones((height, width), dtype=int) * 3  # Giá trị 3 cho tường
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Tùy chỉnh màu sắc
    colors = {
        3: 'black',    # Tường
        0: 'white',    # Đường đi
        1: 'green',    # Ô đã thăm
        2: 'yellow'    # Ô hiện tại
    }
    cmap = plt.cm.colors.ListedColormap([colors[0], colors[1], colors[2], colors[3]])
    norm = plt.Normalize(0, 3)
    im = ax.imshow(maze, cmap=cmap, norm=norm)

    ax.set_title("Kruskal's Maze Generation")
    ax.axis('off')

    # Vẽ lưới
    for i in range(height + 1):
        ax.axhline(i - 0.5, color='black', linewidth=1, zorder=10)
    for j in range(width + 1):
        ax.axvline(j - 0.5, color='black', linewidth=1, zorder=10)

    # Chú thích
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color=colors[3], lw=4, label='Wall'),
        Line2D([0], [0], color=colors[0], lw=4, label='Path'),
        Line2D([0], [0], color=colors[1], lw=4, label='Visited Cell'),
        Line2D([0], [0], color=colors[2], lw=4, label='Current Cell')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=8)

    steps = maze_obj.generation_path
    visited_cells = set()
    current_cells = set()

    def update(frame):
        nonlocal visited_cells, current_cells
        if frame == 0:
            maze[:, :] = 3  # Toàn bộ là tường
        else:
            step = steps[frame - 1]
            if step[0] == "cell":
                maze[step[1], step[2]] = 1  # Ô đã thăm
                visited_cells.add((step[1], step[2]))
            elif step[0] == "current_cells":
                # Đặt lại các ô hiện tại trước đó
                for x, y in current_cells:
                    if (x, y) in visited_cells:
                        maze[x, y] = 1  # Ô đã thăm
                current_cells = set(step[1])
                for x, y in current_cells:
                    maze[x, y] = 2  # Ô hiện tại
            elif step[0] == "break_wall":
                maze[step[1], step[2]] = 0  # Phá tường
                # Đặt lại các ô hiện tại sau khi phá tường
                for x, y in current_cells:
                    if (x, y) in visited_cells:
                        maze[x, y] = 1  # Ô đã thăm
                current_cells.clear()
            elif step[0] == "extra_wall":
                maze[step[1], step[2]] = 0  # Đường đi bổ sung

        im.set_array(maze)
        return [im]

    ani = animation.FuncAnimation(
        fig, update, frames=len(steps) + 1, interval=interval, blit=False, repeat=False
    )
    
    if save_animation:
        ani.save('kruskal_maze.mp4', writer='ffmpeg', fps=30)
        print("Đã lưu animation thành file kruskal_maze.mp4")
    
    plt.show()
    
if __name__ == "__main__":
    size = 10      # Kích thước mê cung cố định
    speed = 10    # Tốc độ animation cố định (ms)
    animate_kruskal_maze(size=size, interval=speed)