import numpy as np
import copy
import os
import time
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
import sys

# Thêm đường dẫn để import các module từ thư mục cha
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maze.maze import Maze
from algorithm.dfs_final import find_path

# Cấu hình màu sắc (đồng bộ với A* và BFS)
COLORS = {
    'background': '#1E1E2E',     # Nền xanh đậm
    'wall': '#4B5EAA',           # Tường màu xanh dương nhạt
    'passage': '#2D3142',        # Đường đi màu xám xanh đậm
    'start': '#00FFAA',          # Điểm bắt đầu màu xanh neon
    'end': '#FF3366',            # Điểm kết thúc màu hồng đậm
    'current': '#33CCFF',        # Ô đang xét màu cyan
    'stack': '#FFD700',          # Ô trong stack màu vàng sáng
    'explored': '#7B68EE',       # Ô đã thăm màu tím trung bình
    'path': '#FF8C00',           # Đường đi màu cam đậm
    'text': '#E0E0E0',           # Chữ màu xám nhạt
    'grid': '#44475A',           # Đường lưới màu xám đậm
    'highlight': '#FF5555',      # Màu nhấn mạnh đỏ nhạt
}

class DFSVisualization:
    """Lớp để trực quan hóa thuật toán DFS với các bước chi tiết."""
    def __init__(self, maze_obj, step_by_step=True):
        """
        Khởi tạo với đối tượng mê cung và tùy chọn hiển thị từng bước.
        
        Args:
            maze_obj: Đối tượng Maze chứa thông tin mê cung.
            step_by_step: Nếu True, lưu lại chi tiết từng bước của thuật toán.
        """
        self.maze = maze_obj
        self.maze_array = maze_obj.maze
        self.start = maze_obj.start
        self.end = maze_obj.end
        self.height, self.width = self.maze_array.shape
        self.step_by_step = step_by_step
        self.search_states = []
        self.path = None
        self._initialize_data_structures()
        
        if step_by_step:
            self._run_dfs_with_steps()
        else:
            self._run_dfs()

    def _initialize_data_structures(self):
        """Khởi tạo các cấu trúc dữ liệu để theo dõi thuật toán."""
        self.visited = np.zeros((self.height, self.width), dtype=bool)
        self.parent = np.zeros((self.height, self.width, 2), dtype=int)
        self.parent.fill(-1)

    def _run_dfs(self):
        """Chạy thuật toán DFS mà không lưu chi tiết từng bước."""
        self.path = find_path(self.maze)

    def _run_dfs_with_steps(self):
        """Chạy thuật toán DFS và lưu chi tiết từng bước."""
        stack = [self.start]
        self.visited[self.start] = True
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        self._save_search_state(
            current=None,
            stack=[self.start],
            explored=[],
            step_description="Khởi tạo: Thêm điểm xuất phát vào ngăn xếp",
            stack_copy=list(stack)
        )

        found = False
        while stack and not found:
            current = stack.pop()
            current_x, current_y = current

            self._save_search_state(
                current=current,
                stack=list(stack),
                explored=[(i, j) for i in range(self.height) for j in range(self.width) 
                          if self.visited[i, j] and (i, j) != current],
                step_description=f"Xét node ({current_x}, {current_y})",
                stack_copy=list(stack)
            )

            if current == self.end:
                found = True
                self._save_search_state(
                    current=current,
                    stack=list(stack),
                    explored=[(i, j) for i in range(self.height) for j in range(self.width) 
                              if self.visited[i, j] and (i, j) != current],
                    step_description=f"Đã tìm thấy đích tại ({current_x}, {current_y})!",
                    stack_copy=list(stack)
                )
                break

            neighbors_checked = []
            for dx, dy in directions:
                next_x, next_y = current_x + dx, current_y + dy
                next_pos = (next_x, next_y)

                if (0 <= next_x < self.height and 0 <= next_y < self.width and
                        self.maze_array[next_x, next_y] == 0 and not self.visited[next_x, next_y]):
                    self.visited[next_x, next_y] = True
                    self.parent[next_x, next_y] = [current_x, current_y]
                    stack.append(next_pos)
                    neighbors_checked.append(next_pos)

                    self._save_search_state(
                        current=current,
                        stack=list(stack),
                        explored=[(i, j) for i in range(self.height) for j in range(self.width) 
                                  if self.visited[i, j] and (i, j) != current],
                        step_description=f"Thêm hàng xóm ({next_x}, {next_y}) vào ngăn xếp",
                        stack_copy=list(stack),
                        neighbor_checking=next_pos
                    )

            self._save_search_state(
                current=None,
                stack=list(stack),
                explored=[(i, j) for i in range(self.height) for j in range(self.width) if self.visited[i, j]],
                step_description=f"Hoàn thành xét node ({current_x}, {current_y}), đã thêm {len(neighbors_checked)} hàng xóm",
                stack_copy=list(stack)
            )

        if found:
            self.path = []
            current = self.end
            while current != self.start:
                self.path.append(current)
                current_x, current_y = current
                parent_x, parent_y = self.parent[current_x, current_y]
                current = (parent_x, parent_y)
                self._save_search_state(
                    current=None,
                    stack=[],
                    explored=[(i, j) for i in range(self.height) for j in range(self.width) if self.visited[i, j]],
                    step_description=f"Tái tạo đường đi: Thêm node ({current_x}, {current_y})",
                    stack_copy=[],
                    path=self.path + [current]
                )
            self.path.append(self.start)
            self.path.reverse()
            self._save_search_state(
                current=None,
                stack=[],
                explored=[(i, j) for i in range(self.height) for j in range(self.width) if self.visited[i, j]],
                step_description=f"Đường đi hoàn chỉnh: {len(self.path)} bước",
                stack_copy=[],
                path=self.path
            )
        else:
            self._save_search_state(
                current=None,
                stack=[],
                explored=[(i, j) for i in range(self.height) for j in range(self.width) if self.visited[i, j]],
                step_description="Không tìm thấy đường đi!",
                stack_copy=[]
            )

    def _save_search_state(self, current, stack, explored, step_description, stack_copy, path=None, neighbor_checking=None):
        """Lưu trạng thái hiện tại của thuật toán."""
        state = {
            'current': current,
            'stack': stack,
            'explored': explored,
            'step_description': step_description,
            'stack_copy': copy.deepcopy(stack_copy),
            'path': path,
            'neighbor_checking': neighbor_checking
        }
        self.search_states.append(state)

    def get_search_states(self):
        """Trả về danh sách các trạng thái tìm kiếm."""
        return self.search_states

    def get_path(self):
        """Trả về đường đi từ điểm bắt đầu đến điểm kết thúc."""
        return self.path

def create_dfs_animation(maze_obj, interval=300, save_animation=True, show_plot=True):
    """
    Tạo animation trực quan hóa thuật toán DFS với chú thích ngang ở dưới.
    
    Args:
        maze_obj: Đối tượng Maze chứa thông tin mê cung.
        interval: Thời gian giữa các frame (ms).
        save_animation: Lưu animation thành file video.
        show_plot: Hiển thị animation trên màn hình.
    """
    dfs_viz = DFSVisualization(maze_obj, step_by_step=True)
    search_states = dfs_viz.get_search_states()
    path = dfs_viz.get_path()
    maze_array = maze_obj.maze
    height, width = maze_array.shape

    print(f"Tạo animation với {len(search_states)} bước...")

    # Thiết lập giao diện với bố cục dọc
    fig = plt.figure(figsize=(10, 8), facecolor=COLORS['background'])
    gs = GridSpec(2, 1, height_ratios=[3, 1], figure=fig, hspace=0.3)
    ax_maze = fig.add_subplot(gs[0])
    ax_maze.set_facecolor(COLORS['background'])
    ax_info = fig.add_subplot(gs[1])
    ax_info.set_facecolor(COLORS['background'])
    ax_info.axis('off')
    fig.suptitle("Trực quan hóa thuật toán DFS", color=COLORS['text'], fontsize=14)

    last_frame_shown = [False]
    pause_start_time = [0]

    def init():
        """Khởi tạo các trục."""
        ax_maze.clear()
        ax_maze.set_facecolor(COLORS['background'])
        ax_maze.set_xticks([])
        ax_maze.set_yticks([])
        ax_info.clear()
        ax_info.set_facecolor(COLORS['background'])
        ax_info.axis('off')
        return []

    def update(frame):
        """Cập nhật frame cho animation."""
        if last_frame_shown[0]:
            if time.time() - pause_start_time[0] < 5:
                return []
            last_frame_shown[0] = False

        ax_maze.clear()
        ax_info.clear()
        ax_info.axis('off')

        state = search_states[frame]
        current = state['current']
        stack = state['stack']
        explored = state['explored']
        step_description = state['step_description']
        path_so_far = state['path']
        neighbor_checking = state['neighbor_checking']

        # Tạo ma trận màu
        rgb_data = np.zeros((height, width, 3))
        for i in range(height):
            for j in range(width):
                rgb_data[i, j] = mcolors.to_rgb(COLORS['wall'] if maze_array[i, j] == 1 else COLORS['passage'])

        for pos in explored:
            rgb_data[pos[0], pos[1]] = mcolors.to_rgb(COLORS['explored'])
        for pos in stack:
            rgb_data[pos[0], pos[1]] = mcolors.to_rgb(COLORS['stack'])
        if neighbor_checking:
            i, j = neighbor_checking
            rgb_data[i, j] = mcolors.to_rgb(COLORS['highlight'])
        if current:
            i, j = current
            rgb_data[i, j] = mcolors.to_rgb(COLORS['current'])
        if path_so_far:
            for pos in path_so_far:
                rgb_data[pos[0], pos[1]] = mcolors.to_rgb(COLORS['path'])
        rgb_data[maze_obj.start] = mcolors.to_rgb(COLORS['start'])
        rgb_data[maze_obj.end] = mcolors.to_rgb(COLORS['end'])

        # Hiệu ứng phóng to cho ô hiện tại
        if current:
            i, j = current
            rect = patches.Rectangle((j-0.4, i-0.4), 0.8, 0.8, linewidth=2, edgecolor=COLORS['highlight'], facecolor='none')
            ax_maze.add_patch(rect)

        ax_maze.imshow(rgb_data)
        for i in range(height + 1):
            ax_maze.axhline(i - 0.5, color=COLORS['grid'], linewidth=1)
        for j in range(width + 1):
            ax_maze.axvline(j - 0.5, color=COLORS['grid'], linewidth=1)

        ax_maze.set_title(f"Bước {frame+1}/{len(search_states)}", color=COLORS['text'], fontsize=10)
        ax_maze.set_xticks([])
        ax_maze.set_yticks([])

        # Thông tin thuật toán và chú thích nằm ngang ở dưới
        ax_info.text(0.0, 0.9, f"Thuật Toán DFS | {step_description}", color=COLORS['text'], fontsize=10, wrap=True)
        ax_info.text(0.0, 0.7, "Depth-First Search | LIFO Stack", color=COLORS['text'], fontsize=8)
        ax_info.text(0.0, 0.6, f"Nodes đã thăm: {len(explored) + (1 if current else 0)} | Stack: {len(stack)}", color=COLORS['text'], fontsize=8)
        if path_so_far:
            ax_info.text(0.0, 0.5, f"Độ dài đường đi: {len(path_so_far) - 1}", color=COLORS['text'], fontsize=8)

        # Chú thích màu sắc nằm ngang
        x_pos = 0.0
        ax_info.text(x_pos, 0.3, "Chú thích:", color=COLORS['text'], fontsize=10)
        for label, color_key in [
            ('Start', 'start'), ('Goal', 'end'), ('Current', 'current'),
            ('Stack', 'stack'), ('Explored', 'explored'), ('Path', 'path'),
            ('Checking', 'highlight')
        ]:
            ax_info.add_patch(patches.Rectangle((x_pos, 0.2), 0.04, 0.03, facecolor=COLORS[color_key]))
            ax_info.text(x_pos + 0.05, 0.215, label, color=COLORS['text'], fontsize=8, va='center')
            x_pos += 0.15

        if frame == len(search_states) - 1:
            if path_so_far:
                ax_info.text(0.5, 0.05, f"ĐƯỜNG ĐI HOÀN TẤT! Độ dài: {len(path_so_far) - 1}", 
                             ha='center', color=COLORS['highlight'], fontsize=10, weight='bold')
            else:
                ax_info.text(0.5, 0.05, "KHÔNG TÌM THẤY ĐƯỜNG!", 
                             ha='center', color=COLORS['highlight'], fontsize=10, weight='bold')
            last_frame_shown[0] = True
            pause_start_time[0] = time.time()

        return []

    ani = FuncAnimation(fig, update, frames=len(search_states), init_func=init, 
                       blit=True, interval=interval, repeat=True)

    if save_animation:
        os.makedirs("results", exist_ok=True)
        filename = "results/dfs_animation.mp4"
        print(f"Đang lưu animation vào {filename}...")
        ani.save(filename, writer='ffmpeg', fps=10, dpi=150, extra_args=['-vcodec', 'libx264'])
        print("Lưu animation thành công!")

    if show_plot:
        plt.tight_layout()
        plt.subplots_adjust(top=0.85, bottom=0.1)
        plt.show()
    else:
        plt.close()

if __name__ == "__main__":
    print("\nAnimation DFS")
    print("1. Tạo mê cung ngẫu nhiên")
    print("2. Sử dụng mê cung có sẵn")
    
    choice = input("\nNhập lựa chọn (1-2): ")
    
    if choice == "1":
        size = int(input("Nhập kích thước mê cung (ví dụ: 10): "))
        complexity = float(input("Nhập độ phức tạp (0-0.1, ví dụ: 0.03): "))
        algorithm = input("Chọn thuật toán tạo mê cung (dfs_backtrack/prim): ")
        print(f"\nĐang tạo mê cung ngẫu nhiên {size}x{size}...")
        maze = Maze(size, complexity=complexity, algorithm=algorithm)
        maze.print_maze()
    elif choice == "2":
        print("\nSử dụng mê cung mặc định...")
        maze = Maze(10, complexity=0.03, algorithm="dfs_backtrack")
        maze.print_maze()
    else:
        print("Lựa chọn không hợp lệ!")
        sys.exit(1)
    
    interval = int(input("\nNhập tốc độ animation (ms, 300 là bình thường): "))
    save = input("Bạn có muốn lưu animation (y/n): ").lower() == 'y'
    create_dfs_animation(maze, interval=interval, save_animation=save, show_plot=True)