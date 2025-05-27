import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.animation as animation
from collections import deque
import sys
import os

def find_path(maze_obj, return_search_steps=False):
    """
    Tìm đường đi từ điểm bắt đầu đến điểm kết thúc trong mê cung bằng DFS.

    Args:
        maze_obj: Instance của lớp Maze, với thuộc tính:
            - maze: Ma trận numpy (0: đường đi, 1: tường).
            - start: Tọa độ (x, y) của điểm bắt đầu.
            - end: Tọa độ (x, y) của điểm kết thúc.
        return_search_steps: Nếu True, trả về các bước tìm kiếm và trạng thái stack.

    Returns:
        tuple:
            - path: List tọa độ (x, y) từ start đến end, hoặc None nếu không có đường.
            - steps: Tuple (search_steps, stack_steps) nếu return_search_steps=True, với:
                - search_steps: List tọa độ (x, y) theo thứ tự thăm.
                - stack_steps: List các trạng thái stack (danh sách tọa độ).
            - error: String mô tả lỗi (nếu có, ví dụ: "No path exists"), hoặc None nếu thành công.

    Complexity:
        - Time: O(V + E), với V là số ô, E là số cạnh.
        - Space: O(V) cho visited, parent, stack, và search_steps.
    """
    maze = maze_obj.maze
    start_pos = maze_obj.start
    end_pos = maze_obj.end
    height, width = maze.shape

    visited = np.zeros((height, width), dtype=bool)
    parent = np.full((height, width, 2), -1, dtype=int)
    stack = deque([start_pos])
    visited[start_pos] = True

    search_steps = [start_pos] if return_search_steps else None
    stack_steps = [list(stack)] if return_search_steps else None
    search_steps_set = {start_pos} if return_search_steps else None

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    found = False

    while stack and not found:
        current_pos = stack.pop()
        current_x, current_y = current_pos

        if return_search_steps and current_pos not in search_steps_set:
            search_steps.append(current_pos)
            search_steps_set.add(current_pos)
            stack_steps.append(list(stack))

        if current_pos == end_pos:
            found = True
            if return_search_steps:
                stack_steps.append(list(stack))
            break

        for dx, dy in directions:
            next_x, next_y = current_x + dx, current_y + dy
            next_pos = (next_x, next_y)
            if (0 <= next_x < height and 0 <= next_y < width and
                    maze[next_x, next_y] == 0 and not visited[next_x, next_y]):
                stack.append(next_pos)
                visited[next_x, next_y] = True
                parent[next_x, next_y] = [current_x, current_y]
                if return_search_steps:
                    stack_steps.append(list(stack))

    if found:
        path = []
        current_pos = end_pos
        while current_pos != start_pos:
            path.append(current_pos)
            curr_x, curr_y = current_pos
            current_pos = tuple(parent[curr_x, curr_y])
            if current_pos == (-1, -1):
                break
        path.append(start_pos)
        path.reverse()
        if return_search_steps:
            return path, (search_steps, stack_steps), None
        return path, None
    else:
        error = "No path exists between start and end"
        if return_search_steps:
            return None, (search_steps, stack_steps), error
        return None, error

def print_maze_with_path(maze_obj, path):
    """
    In mê cung ra console với đường đi được biểu diễn bằng '-'.

    Args:
        maze_obj: Instance của lớp Maze.
        path: List tọa độ (x, y) thể hiện đường đi.
    """
    if path is None:
        print("Không tìm thấy đường đi!")
        return

    maze_display = maze_obj.maze.copy()
    for x, y in path:
        maze_display[x, y] = 2

    for row in maze_display:
        print(''.join('#' if cell == 1 else '-' if cell == 2 else ' ' for cell in row))

def visualize_maze_with_path(maze_obj, path):
    """
    Trực quan hóa mê cung tĩnh với đường đi được đánh dấu, sử dụng màu sắc giống Pygame.

    Args:
        maze_obj: Instance của lớp Maze.
        path: List tọa độ (x, y) thể hiện đường đi.
    """
    maze = maze_obj.maze
    height, width = maze.shape

    # Màu sắc giống Pygame
    COLORS = {
        'background': '#FFFFFF',  # Trắng
        'wall': '#000000',        # Đen
        'path': '#800080',        # Tím
        'start': '#0000FF',       # Xanh dương
        'end': '#FFA500',         # Cam
        'grid': '#000000'         # Lưới đen
    }

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_facecolor(COLORS['background'])

    # Vẽ mê cung
    rgb_data = np.ones((height, width, 3))  # Nền trắng
    for i in range(height):
        for j in range(width):
            if maze[i, j] == 1:
                rgb_data[i, j] = np.array([0, 0, 0])  # Tường đen

    ax.imshow(rgb_data)

    # Vẽ lưới đen
    for i in range(height + 1):
        ax.axhline(i - 0.5, color=COLORS['grid'], linewidth=2)
    for j in range(width + 1):
        ax.axvline(j - 0.5, color=COLORS['grid'], linewidth=2)

    # Vẽ đường đi
    if path:
        path_x = [y for x, y in path]
        path_y = [x for x, y in path]
        ax.plot(path_x, path_y, color=COLORS['path'], linewidth=2)
        ax.plot(path_x, path_y, 'o', color=COLORS['path'], markersize=3)

    # Vẽ start và end
    start_pos = maze_obj.start
    end_pos = maze_obj.end
    ax.plot(start_pos[1], start_pos[0], 'o', color=COLORS['start'], markersize=8, label='Start')
    ax.plot(end_pos[1], end_pos[0], 'o', color=COLORS['end'], markersize=8, label='End')

    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(-0.5, height - 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.invert_yaxis()
    ax.set_aspect('equal')
    plt.title('DFS Maze Solution' if path else 'Maze (No Path Found)')
    plt.legend()
    plt.tight_layout()
    plt.show()

def create_dfs_animation(maze_obj, interval=100, save_animation=False, show_plot=True):
    """
    Tạo animation trực quan hóa thuật toán DFS với giao diện giống Pygame.

    Args:
        maze_obj: Instance của lớp Maze chứa thông tin mê cung.
        interval: Thời gian giữa các frame (ms).
        save_animation: Lưu animation thành file video.
        show_plot: Hiển thị animation trên màn hình.

    Returns:
        tuple: (path, (search_steps, stack_steps), error) từ find_path.
    """
    result = find_path(maze_obj, return_search_steps=True)
    path, (search_steps, stack_steps), error = result

    if not search_steps:
        if show_plot:
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.text(0.5, 0.5, "No search steps to visualize!", ha='center', va='center', fontsize=12, color='red')
            ax.set_axis_off()
            plt.show()
        return path, (search_steps, stack_steps), error

    maze = maze_obj.maze
    height, width = maze.shape

    # Màu sắc giống Pygame
    COLORS = {
        'background': '#FFFFFF',  # Trắng
        'wall': '#000000',        # Đen
        'start': '#0000FF',       # Xanh dương
        'end': '#FFA500',         # Cam
        'current': '#40E0D0',     # Turquoise
        'stack': '#00FF00',       # Xanh lá
        'explored': '#FF0000',    # Đỏ
        'path': '#800080',        # Tím
        'grid': '#000000'         # Lưới đen
    }

    fig = plt.figure(figsize=(10, 10), facecolor=COLORS['background'])
    ax = fig.add_subplot(111)
    ax.set_facecolor(COLORS['background'])

    # Vẽ mê cung
    rgb_data = np.ones((height, width, 3))  # Nền trắng
    for i in range(height):
        for j in range(width):
            if maze[i, j] == 1:
                rgb_data[i, j] = np.array([0, 0, 0])  # Tường đen

    ax.imshow(rgb_data)

    # Vẽ lưới đen
    for i in range(height + 1):
        ax.axhline(i - 0.5, color=COLORS['grid'], linewidth=2)
    for j in range(width + 1):
        ax.axvline(j - 0.5, color=COLORS['grid'], linewidth=2)

    # Vẽ start và end
    start_pos = maze_obj.start
    end_pos = maze_obj.end
    ax.plot(start_pos[1], start_pos[0], 'o', color=COLORS['start'], markersize=8)
    ax.plot(end_pos[1], end_pos[0], 'o', color=COLORS['end'], markersize=8)

    # Khởi tạo các plot
    explored_plot, = ax.plot([], [], 'o', color=COLORS['explored'], markersize=4, alpha=0.4)
    current_plot, = ax.plot([], [], 'o', color=COLORS['current'], markersize=7, alpha=0.8)
    stack_plot, = ax.plot([], [], 'o', color=COLORS['stack'], markersize=4, alpha=0.6)
    path_plot, = ax.plot([], [], color=COLORS['path'], linewidth=2)
    path_markers, = ax.plot([], [], 'o', color=COLORS['path'], markersize=4)

    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(-0.5, height - 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.invert_yaxis()
    ax.set_aspect('equal')

    title = ax.set_title('Tìm kiếm DFS: Bước 0')
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['start'], markersize=8, label='Điểm bắt đầu'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['end'], markersize=8, label='Điểm kết thúc'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['current'], markersize=8, label='Đang xét'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['stack'], markersize=8, label='Trong Stack'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['explored'], markersize=8, label='Đã xét'),
        plt.Line2D([0], [0], color=COLORS['path'], label='Đường đi')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize='small')

    explored_x, explored_y = [], []

    def init():
        current_plot.set_data([], [])
        explored_plot.set_data([], [])
        stack_plot.set_data([], [])
        path_plot.set_data([], [])
        path_markers.set_data([], [])
        title.set_text('Tìm kiếm DFS: Bước 0')
        return current_plot, explored_plot, stack_plot, path_plot, path_markers, title

    def update(frame):
        if frame < len(search_steps):
            current_cell = search_steps[frame]
            current_plot.set_data([current_cell[1]], [current_cell[0]])

            if frame > 0:
                explored_x.append(search_steps[frame-1][1])
                explored_y.append(search_steps[frame-1][0])
                explored_plot.set_data(explored_x, explored_y)
            else:
                explored_plot.set_data([], [])

            if frame < len(stack_steps):
                stack_y = [y for x, y in stack_steps[frame]]
                stack_x = [x for x, y in stack_steps[frame]]
                stack_plot.set_data(stack_y, stack_x)
            else:
                stack_plot.set_data([], [])

            path_plot.set_data([], [])
            path_markers.set_data([], [])
            title.set_text(f'Tìm kiếm DFS: Bước {frame+1}/{len(search_steps)}')
        else:
            current_plot.set_data([], [])
            if search_steps:
                explored_plot.set_data(explored_x, explored_y)
            stack_plot.set_data([], [])
            if path:
                path_y = [y for x, y in path]
                path_x = [x for x, y in path]
                path_plot.set_data(path_y, path_x)
                path_markers.set_data(path_y, path_x)
                title.set_text(f'Đường đi DFS: {len(path)} bước')
            else:
                title.set_text('Không tìm thấy đường đi (DFS)!')

        return current_plot, explored_plot, stack_plot, path_plot, path_markers, title

    num_frames = len(search_steps) + (10 if path else 0)
    anim = animation.FuncAnimation(fig, update, frames=num_frames, init_func=init,
                                   blit=True, interval=interval, repeat=False)

    if save_animation:
        os.makedirs("results", exist_ok=True)
        filename = "results/dfs_animation.mp4"
        print(f"Đang lưu animation vào {filename}...")
        anim.save(filename, writer='ffmpeg', fps=10, dpi=150, extra_args=['-vcodec', 'libx264'])
        print("Lưu animation thành công!")

    if show_plot:
        plt.tight_layout()
        plt.show()
    else:
        plt.close()

    return path, (search_steps, stack_steps), error

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from maze.maze import Maze
    import time

    maze = Maze(10, complexity=0.03, algorithm="dfs_backtrack")
    print("Mê cung ban đầu:")
    maze.print_maze()
    print("\n")

    show_animation = True
    if show_animation:
        path, steps, error = create_dfs_animation(maze, interval=100, save_animation=False, show_plot=True)
        if error:
            print(f"Không tìm thấy đường đi! Lỗi: {error}")
    else:
        start_time = time.time()
        path, error = find_path(maze)
        end_time = time.time()

        if path:
            print(f"Tìm thấy đường đi với {len(path)} bước:")
            print(f"Độ dài đường đi: {len(path) - 1}")
            print(f"Thời gian thực thi: {end_time - start_time:.5f} giây")
            print_maze_with_path(maze, path)
            visualize_maze_with_path(maze, path)
        else:
            print(f"Không tìm thấy đường đi! Lỗi: {error}")
            print(f"Thời gian thực thi: {end_time - start_time:.5f} giây")