import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
import matplotlib.animation as animation
from collections import deque
import heapq
import sys
import os

def find_path(maze_obj, return_search_steps=False):
    maze = maze_obj.maze
    start_pos = maze_obj.start
    end_pos = maze_obj.end
    height, width = maze.shape

    # Cấu trúc dữ liệu cho A*
    visited = np.zeros((height, width), dtype=bool)
    parent = np.full((height, width, 2), -1, dtype=int)
    g_score = np.full((height, width), np.inf)
    g_score[start_pos] = 0
    f_score = np.full((height, width), np.inf)
    f_score[start_pos] = manhattan_distance(start_pos, end_pos)
    
    # Hàng đợi ưu tiên cho A*
    count = 0
    open_set = [(f_score[start_pos], 0, count, start_pos)]
    heapq.heapify(open_set)
    
    # Theo dõi các bước tìm kiếm
    search_steps = [start_pos] if return_search_steps else None
    open_set_steps = [[(f_score[start_pos], 0, count, start_pos)]] if return_search_steps else None
    search_steps_set = {start_pos} if return_search_steps else None

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    found = False

    while open_set and not found:
        # Lấy nút có f_score thấp nhất
        _, current_g, _, current_pos = heapq.heappop(open_set)
        current_x, current_y = current_pos
        
        # Bỏ qua nếu đã thăm
        if visited[current_x, current_y]:
            if return_search_steps:
                open_set_steps.append(list(open_set))
            continue
            
        # Thêm vào bước tìm kiếm
        if return_search_steps and current_pos not in search_steps_set:
            search_steps.append(current_pos)
            search_steps_set.add(current_pos)
            
        # Đánh dấu là đã thăm
        visited[current_x, current_y] = True
        
        # Kiểm tra nếu đã đến đích
        if current_pos == end_pos:
            found = True
            if return_search_steps:
                open_set_steps.append(list(open_set))
            break
            
        # Kiểm tra tất cả láng giềng
        for dx, dy in directions:
            next_x, next_y = current_x + dx, current_y + dy
            next_pos = (next_x, next_y)
            
            if (0 <= next_x < height and 0 <= next_y < width and
                maze[next_x, next_y] == 0 and not visited[next_x, next_y]):
                
                # Tính g_score mới
                tentative_g_score = g_score[current_x, current_y] + 1
                
                # Nếu g_score mới tốt hơn, cập nhật
                if tentative_g_score < g_score[next_x, next_y]:
                    parent[next_x, next_y] = [current_x, current_y]
                    g_score[next_x, next_y] = tentative_g_score
                    f_score[next_x, next_y] = tentative_g_score + manhattan_distance(next_pos, end_pos)
                    
                    # Thêm vào open_set
                    count += 1
                    heapq.heappush(open_set, (f_score[next_x, next_y], tentative_g_score, count, next_pos))
        
        if return_search_steps:
            open_set_steps.append(list(open_set))
    
    # Tạo đường đi nếu tìm thấy
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
            return path, (search_steps, open_set_steps), None
        return path, None
    else:
        error = "No path exists between start and end"
        if return_search_steps:
            return None, (search_steps, open_set_steps), error
        return None, error

def manhattan_distance(pos1, pos2):
    """Tính khoảng cách Manhattan giữa hai điểm."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

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
    plt.title('A* Maze Solution' if path else 'Maze (No Path Found)')
    plt.legend()
    plt.tight_layout()
    plt.show()

def create_astar_animation(maze_obj, interval=100, save_animation=False, show_plot=True):
    result = find_path(maze_obj, return_search_steps=True)
    path, (search_steps, open_set_steps), error = result

    if not search_steps:
        if show_plot:
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.text(0.5, 0.5, "No search steps to visualize!", ha='center', va='center', fontsize=12, color='red')
            ax.set_axis_off()
            plt.show()
        return path, (search_steps, open_set_steps), error

    maze = maze_obj.maze
    height, width = maze.shape

    COLORS = {
        'background': '#FFFFFF',
        'wall': '#000000',
        'start': '#0000FF',
        'end': '#FFA500',
        'current': '#40E0D0',
        'frontier': '#00FF00',  # Open set trong A*
        'explored': '#FF0000',
        'path': '#800080',
        'grid': '#000000'
    }

    fig = plt.figure(figsize=(10, 10), facecolor=COLORS['background'])
    ax = fig.add_subplot(111)
    ax.set_facecolor(COLORS['background'])

    # Vẽ mê cung
    rgb_data = np.ones((height, width, 3))
    for i in range(height):
        for j in range(width):
            if maze[i, j] == 1:
                rgb_data[i, j] = np.array([0, 0, 0])
    ax.imshow(rgb_data)

    # Vẽ lưới
    for i in range(height + 1):
        ax.axhline(i - 0.5, color=COLORS['grid'], linewidth=2)
    for j in range(width + 1):
        ax.axvline(j - 0.5, color=COLORS['grid'], linewidth=2)

    # Vẽ điểm bắt đầu và kết thúc
    start_pos = maze_obj.start
    end_pos = maze_obj.end
    ax.add_patch(Rectangle((start_pos[1] - 0.5, start_pos[0] - 0.5), 1, 1, facecolor=COLORS['start'], alpha=1.0, zorder=1))
    ax.add_patch(Rectangle((end_pos[1] - 0.5, end_pos[0] - 0.5), 1, 1, facecolor=COLORS['end'], alpha=1.0, zorder=1))

    # Khởi tạo các patch
    explored_patches = []
    current_patch = None
    frontier_patches = []
    path_patches = []

    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(-0.5, height - 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.invert_yaxis()
    ax.set_aspect('equal')

    # Chú thích (legend) với màu sắc và alpha chính xác
    legend_elements = [
        Patch(facecolor=COLORS['start'], edgecolor='none', alpha=1.0, label='Điểm bắt đầu'),
        Patch(facecolor=COLORS['end'], edgecolor='none', alpha=1.0, label='Điểm kết thúc'),
        Patch(facecolor=COLORS['current'], edgecolor='none', alpha=0.8, label='Đang xét'),
        Patch(facecolor=COLORS['frontier'], edgecolor='none', alpha=0.6, label='Trong Open Set'),
        Patch(facecolor=COLORS['explored'], edgecolor='none', alpha=0.4, label='Đã xét'),
        Patch(facecolor=COLORS['path'], edgecolor='none', alpha=0.8, label='Đường đi')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10, frameon=True, edgecolor='black')

    title = ax.set_title('Tìm kiếm A*: Bước 0')

    def init():
        nonlocal current_patch, explored_patches, frontier_patches, path_patches
        for patch in explored_patches + frontier_patches + ([current_patch] if current_patch else []) + path_patches:
            if patch:
                patch.remove()
        explored_patches.clear()
        frontier_patches.clear()
        path_patches.clear()
        current_patch = None
        title.set_text('Tìm kiếm A*: Bước 0')
        return []

    def update(frame):
        nonlocal current_patch, explored_patches, frontier_patches, path_patches
        # Chỉ xóa frontier_patches và path_patches, giữ explored_patches và current_patch
        for patch in frontier_patches + path_patches:
            if patch:
                patch.remove()
        if current_patch:
            current_patch.remove()
        frontier_patches.clear()
        path_patches.clear()
        current_patch = None

        if frame < len(search_steps):
            current_cell = search_steps[frame]
            current_patch = Rectangle((current_cell[1] - 0.5, current_cell[0] - 0.5), 1, 1, 
                                    facecolor=COLORS['current'], alpha=0.8, zorder=3)
            ax.add_patch(current_patch)

            if frame > 0:
                prev_cell = search_steps[frame-1]
                if prev_cell not in [start_pos, end_pos]:  # Không ghi đè điểm bắt đầu/kết thúc
                    explored_patches.append(Rectangle((prev_cell[1] - 0.5, prev_cell[0] - 0.5), 1, 1, 
                                                   facecolor=COLORS['explored'], alpha=0.4, zorder=1))
                    ax.add_patch(explored_patches[-1])

            if frame < len(open_set_steps):
                for _, _, _, pos in open_set_steps[frame]:
                    if pos not in [start_pos, end_pos]:  # Không ghi đè điểm bắt đầu/kết thúc
                        frontier_patches.append(Rectangle((pos[1] - 0.5, pos[0] - 0.5), 1, 1, 
                                                      facecolor=COLORS['frontier'], alpha=0.6, zorder=2))
                        ax.add_patch(frontier_patches[-1])

            title.set_text(f'Tìm kiếm A*: Bước {frame+1}/{len(search_steps)}')
        else:
            if path:
                for cell in path:
                    if cell not in [start_pos, end_pos]:  # Không ghi đè điểm bắt đầu/kết thúc
                        path_patches.append(Rectangle((cell[1] - 0.5, cell[0] - 0.5), 1, 1, 
                                                   facecolor=COLORS['path'], alpha=0.8, zorder=2))
                        ax.add_patch(path_patches[-1])
                title.set_text(f'Đường đi A*: {len(path)} bước')
            else:
                title.set_text('Không tìm thấy đường đi (A*)!')

        return [current_patch] + explored_patches + frontier_patches + path_patches + [title]

    num_frames = len(search_steps) + (10 if path else 0)
    anim = animation.FuncAnimation(fig, update, frames=num_frames, init_func=init,
                                   blit=False, interval=interval, repeat=False)

    if save_animation:
        os.makedirs("results", exist_ok=True)
        filename = "results/astar_animation.mp4"
        print(f"Đang lưu animation vào {filename}...")
        anim.save(filename, writer='ffmpeg', fps=10, dpi=150, extra_args=['-vcodec', 'libx264'])
        print("Lưu animation thành công!")

    if show_plot:
        plt.tight_layout()
        plt.savefig('maze_animation.png')  # Lưu ảnh để kiểm tra
        plt.show()
    else:
        plt.close()

    return path, (search_steps, open_set_steps), error

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
        path, steps, error = create_astar_animation(maze, interval=100, save_animation=False, show_plot=True)
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