import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maze import Maze

def animate_dfs_maze(size=15, interval=100):
    maze_obj = Maze(size, algorithm="dfs_backtrack")
    height, width = maze_obj.maze.shape
    maze = np.ones((height, width), dtype=int)
    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(maze, cmap='binary', vmin=0, vmax=1)

    ax.set_title("DFS Backtrack Maze Generation")
    ax.axis('off')

    steps = maze_obj.generation_path

    # Vẽ lưới một lần duy nhất
    for i in range(height + 1):
        ax.axhline(i - 0.5, color='black', linewidth=1.2, zorder=10)
    for j in range(width + 1):
        ax.axvline(j - 0.5, color='black', linewidth=1.2, zorder=10)

    # Thêm frame đầu tiên là trạng thái ban đầu (toàn tường)
    def update(frame):
        if frame == 0:
            maze[:, :] = 1  # Toàn bộ là tường
        else:
            step = steps[frame - 1]
            if step[0] == "cell":
                maze[step[1], step[2]] = 0
            elif step[0] == "wall":
                maze[step[1], step[2]] = 0
        im.set_array(maze)
        return [im]

    ani = animation.FuncAnimation(
        fig, update, frames=len(steps) + 1, interval=interval, blit=False, repeat=False
    )
    plt.show()

if __name__ == "__main__":
    size = 10      # Kích thước mê cung cố định
    speed = 10    # Tốc độ animation cố định (ms)
    animate_dfs_maze(size=size, interval=speed)