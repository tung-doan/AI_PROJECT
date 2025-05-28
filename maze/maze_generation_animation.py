import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import os

# Import lớp Maze
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maze import Maze

def create_maze_generation_animation(size=10, complexity=0.03, algorithm="dfs_backtrack", interval=10, save_animation=False, show_plot=True, max_frames=500):
    """
    Tạo animation minh họa quá trình tạo mê cung với hiệu suất cải tiến.

    Args:
        size: int - kích thước mê cung (size x size).
        complexity: float - độ phức tạp của mê cung (nên < 0.1).
        algorithm: str - thuật toán tạo mê cung ("dfs_backtrack" hoặc "prim").
        interval: int - thời gian giữa các frame (ms).
        save_animation: bool - lưu animation thành video.
        show_plot: bool - hiển thị animation trên màn hình.
        max_frames: int - số frame tối đa để giới hạn animation.

    Returns:
        maze_obj: Instance của lớp Maze chứa mê cung đã tạo.
    """
    # Tạo mê cung
    maze_obj = Maze(size, complexity=complexity, algorithm=algorithm)
    generation_steps = maze_obj.generation_path
    maze = maze_obj.maze
    height, width = maze.shape

    # Giảm số bước bằng cách gộp
    optimized_steps = []
    skip_wall_candidates = algorithm == "prim"
    current_step = None
    for step in generation_steps[:max_frames]:
        step_type, x, y = step
        if skip_wall_candidates and step_type == "wall_candidate":
            continue
        if current_step and current_step[0] in ("cell", "wall"):
            optimized_steps.append(current_step)
        current_step = (step_type, x, y)
    if current_step:
        optimized_steps.append(current_step)

    # Màu sắc giống Pygame
    COLORS = {
        'background': '#FFFFFF',  # Trắng
        'wall': '#000000',        # Đen
        'path': '#800080',        # Tím
        'current': '#40E0D0',     # Turquoise
        'wall_candidate': '#00FF00',  # Xanh lá
        'grid': '#000000'         # Lưới đen
    }

    # Khởi tạo figure
    fig = plt.figure(figsize=(8, 8), facecolor=COLORS['background'])
    ax = fig.add_subplot(111)
    ax.set_facecolor(COLORS['background'])

    # Khởi tạo mê cung
    rgb_data = np.ones((height, width, 3))  # Toàn tường
    img = ax.imshow(rgb_data, animated=True)

    # Vẽ lưới
    for i in range(height + 1):
        ax.axhline(i - 0.5, color=COLORS['grid'], linewidth=1)
    for j in range(width + 1):
        ax.axvline(j - 0.5, color=COLORS['grid'], linewidth=1)

    # Plot cho ô hiện tại
    current_plot, = ax.plot([], [], 'o', color=COLORS['current'], markersize=6)

    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(-0.5, height - 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.invert_yaxis()
    ax.set_aspect('equal')

    title = ax.set_title(f'Tạo mê cung ({algorithm}): Bước 0')
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['current'], markersize=6, label='Ô hiện tại'),
        plt.Line2D([0], [0], color=COLORS['path'], label='Đường đi')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize='small')

    def init():
        rgb_data[:] = 1
        img.set_array(rgb_data)
        current_plot.set_data([], [])
        title.set_text(f'Tạo mê cung ({algorithm}): Bước 0')
        return img, current_plot, title

    def update(frame):
        if frame >= len(optimized_steps):
            title.set_text(f'Mê cung hoàn thành ({algorithm})')
            current_plot.set_data([], [])
            return img, current_plot, title

        step_type, x, y = optimized_steps[frame]
        if step_type in ("cell", "wall"):
            rgb_data[x, y] = np.array([128/255, 0, 128/255])  # Tím
            current_plot.set_data([y], [x] if step_type == "cell" else [[], []])
        img.set_array(rgb_data)
        title.set_text(f'Tạo mê cung ({algorithm}): Bước {frame+1}/{len(optimized_steps)}')
        return img, current_plot, title

    anim = animation.FuncAnimation(fig, update, frames=len(optimized_steps) + 10,
                                   init_func=init, blit=True, interval=interval, repeat=False)

    if save_animation:
        os.makedirs("results", exist_ok=True)
        filename = f"results/maze_generation_{algorithm}.mp4"
        print(f"Đang lưu animation vào {filename}...")
        anim.save(filename, writer='ffmpeg', fps=60, dpi=100, extra_args=['-vcodec', 'libx264'])
        print("Lưu animation thành công!")

    if show_plot:
        plt.tight_layout()
        plt.show()
    else:
        plt.close()

    return maze_obj

if __name__ == "__main__":
    try:
        maze = create_maze_generation_animation(size=10, complexity=0.03, algorithm="dfs_backtrack", interval=10, max_frames=500)
        print("\nMê cung cuối cùng:")
        maze.print_maze()
    except Exception as e:
        print(f"Lỗi: {e}")
    input("Nhấn Enter để đóng...")