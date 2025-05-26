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
from maze.maze import Maze

"""
File này tạo animation chi tiết phong cách 3Blue1Brown cho quá trình tạo mê cung
với các hiệu ứng chuyển động mượt mà và chú thích rõ ràng
"""

# Định nghĩa bảng màu đẹp mắt phong cách 3Blue1Brown
COLORS = {
    'background': '#000000',     # Nền đen
    'wall': '#444444',           # Tường màu xám đậm
    'passage': '#FFFFFF',        # Đường đi màu trắng
    'current': '#3B7EA1',        # Ô đang xét màu xanh 3Blue1Brown
    'visited': '#8A97C8',        # Ô đã thăm màu tím nhạt
    'backtrack': '#E07A5F',      # Ô đang backtrack màu cam
    'frontier': '#F2CC8F',       # Ô biên giới màu vàng
    'highlight': '#F94144',      # Màu nhấn mạnh đỏ
    'start': '#81B29A',          # Điểm bắt đầu màu xanh lá
    'end': '#F3722C',            # Điểm kết thúc màu cam
    'text': '#FFFFFF',           # Chữ màu trắng
    'grid': '#252525',           # Đường lưới màu xám nhạt
    'arrow': '#F9C74F',          # Mũi tên màu vàng
}

class MazeWithDetailedSteps(Maze):
    def __init__(self, size, complexity=0.0, algorithm="dfs_backtrack"):
        """
        Khởi tạo mê cung với khả năng ghi lại chi tiết từng bước nhỏ
        trong quá trình tạo mê cung
        """
        self.size = size
        self.complexity = complexity
        self.algorithm = algorithm
        
        # Khởi tạo mê cung với toàn bộ là tường (1)
        width = 2*self.size + 1
        height = 2*self.size + 1
        self.maze = np.ones((height, width), dtype=int)
        
        # Thiết lập điểm bắt đầu và kết thúc
        self.start = (1, 1)
        self.end = (2*size - 1, 2*size - 1)
        
        # Cấu trúc dữ liệu lưu trữ chi tiết từng bước trong quá trình tạo mê cung
        # Mỗi bước sẽ bao gồm:
        # - maze_state: trạng thái hiện tại của mê cung
        # - cell_types: trạng thái của từng ô (đường đi, tường, ô hiện tại, ô đã thăm...)
        # - algorithm_state: thông tin về thuật toán (stack, frontier, etc.)
        # - description: mô tả hành động đang thực hiện
        self.detailed_steps = []
        
        # Tạo mê cung và ghi lại các bước
        self.generate_maze_with_detailed_steps()
        
    def generate_maze_with_detailed_steps(self):
        """
        Tạo mê cung và ghi lại từng bước nhỏ
        """
        if self.algorithm == "dfs_backtrack":
            self._dfs_backtrack_maze_detailed()
        elif self.algorithm == "prim":
            self._prim_maze_detailed()
        else:
            self._dfs_backtrack_maze_detailed()
        
        # Thêm điểm bắt đầu và kết thúc
        self.maze[self.start[0]][self.start[1]] = 0
        self.maze[self.end[0]][self.end[1]] = 0
        
        # Thêm trạng thái cuối cùng
        width = 2*self.size + 1
        height = 2*self.size + 1
        
        final_cell_types = np.full((height, width), 'wall', dtype=object)
        for i in range(height):
            for j in range(width):
                if self.maze[i][j] == 0:
                    final_cell_types[i][j] = 'passage'
        
        final_cell_types[self.start[0]][self.start[1]] = 'start'
        final_cell_types[self.end[0]][self.end[1]] = 'end'
        
        self.detailed_steps.append({
            'maze_state': copy.deepcopy(self.maze),
            'cell_types': final_cell_types,
            'algorithm_state': {},
            'description': 'Mê cung hoàn chỉnh với điểm bắt đầu (xanh) và điểm kết thúc (cam)'
        })
    
    def _dfs_backtrack_maze_detailed(self):
        """
        Tạo mê cung sử dụng thuật toán DFS Backtracker và ghi lại chi tiết từng bước
        """
        width = 2*self.size + 1
        height = 2*self.size + 1
        
        # Mảng để đánh dấu các ô đã thăm
        visited = np.zeros((self.size, self.size), dtype=bool)
        
        # Khởi tạo cell_types để theo dõi trạng thái của từng ô
        cell_types = np.full((height, width), 'wall', dtype=object)
        
        # Chọn một vị trí bắt đầu ngẫu nhiên (giống hệt maze.py)
        start_x = random.randint(0, self.size-1)
        start_y = random.randint(0, self.size-1)
        
        # Đánh dấu ô bắt đầu đã thăm
        visited[start_x][start_y] = True
        
        # Chuyển đổi tọa độ logic sang tọa độ ma trận
        cell_x = 2*start_x + 1
        cell_y = 2*start_y + 1
        
        # Đánh dấu ô hiện tại là đường đi
        self.maze[cell_x][cell_y] = 0
        cell_types[cell_x][cell_y] = 'current'
        
        # Stack để lưu trữ các ô đã thăm để backtracking
        stack = [(start_x, start_y)]
        
        # Lưu trạng thái ban đầu
        self.detailed_steps.append({
            'maze_state': copy.deepcopy(self.maze),
            'cell_types': copy.deepcopy(cell_types),
            'algorithm_state': {
                'stack': copy.deepcopy(stack),
                'visited': copy.deepcopy(visited)
            },
            'description': 'Bắt đầu tạo mê cung với một ô ngẫu nhiên'
        })
        
        # Đếm số ô đã thăm
        visit_counter = 1
        
        # Lặp cho đến khi tất cả các ô đều được thăm
        while visit_counter < self.size * self.size:
            x, y = stack[-1]  # Lấy ô hiện tại từ đỉnh stack
            cell_x, cell_y = 2*x + 1, 2*y + 1
            
            # Cập nhật cell_types - đổi ô hiện tại thành đã thăm
            for i in range(height):
                for j in range(width):
                    if cell_types[i][j] == 'current':
                        cell_types[i][j] = 'visited'
            
            # Đánh dấu ô hiện tại
            cell_types[cell_x][cell_y] = 'current'
            
            # Tìm tất cả các hàng xóm chưa thăm - chính xác như maze.py
            neighbors = []
            for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if 0 <= nx < self.size and 0 <= ny < self.size and not visited[nx][ny]:
                    neighbors.append((nx, ny))
            
            # Đánh dấu các hàng xóm chưa thăm là frontier
            for nx, ny in neighbors:
                ncell_x, ncell_y = 2*nx + 1, 2*ny + 1
                cell_types[ncell_x][ncell_y] = 'frontier'
            
            # Lưu trạng thái: Đang xem xét ô hiện tại và các hàng xóm
            self.detailed_steps.append({
                'maze_state': copy.deepcopy(self.maze),
                'cell_types': copy.deepcopy(cell_types),
                'algorithm_state': {
                    'stack': copy.deepcopy(stack),
                    'visited': copy.deepcopy(visited),
                    'neighbors': copy.deepcopy(neighbors)
                },
                'description': f'Đang xem xét ô ({x},{y}) với {len(neighbors)} hàng xóm chưa thăm'
            })
            
            if neighbors:  # Nếu có hàng xóm chưa thăm
                # Chọn một hàng xóm ngẫu nhiên - sử dụng random.choice giống maze.py
                next_x, next_y = random.choice(neighbors)
                
                # Đánh dấu hàng xóm đã thăm
                visited[next_x][next_y] = True
                visit_counter += 1
                
                # Xóa tường giữa ô hiện tại và hàng xóm - công thức chính xác từ maze.py
                wall_x = 2*x + 1 + (next_x - x)
                wall_y = 2*y + 1 + (next_y - y)
                self.maze[wall_x][wall_y] = 0
                cell_types[wall_x][wall_y] = 'passage'
                
                # Đánh dấu ô hàng xóm là đường đi
                cell_x = 2*next_x + 1
                cell_y = 2*next_y + 1
                self.maze[cell_x][cell_y] = 0
                
                # Cập nhật cell_types - đổi tất cả frontier thành wall ngoại trừ ô được chọn
                for i in range(height):
                    for j in range(width):
                        if cell_types[i][j] == 'frontier' and (i != cell_x or j != cell_y):
                            cell_types[i][j] = 'wall'
                
                # Đánh dấu ô được chọn là current mới
                cell_types[cell_x][cell_y] = 'current'
                
                # Thêm hàng xóm vào stack - giống maze.py
                stack.append((next_x, next_y))
                
                # Lưu trạng thái: Đã chọn hàng xóm và di chuyển tới đó
                self.detailed_steps.append({
                    'maze_state': copy.deepcopy(self.maze),
                    'cell_types': copy.deepcopy(cell_types),
                    'algorithm_state': {
                        'stack': copy.deepcopy(stack),
                        'visited': copy.deepcopy(visited),
                        'chosen_neighbor': (next_x, next_y)
                    },
                    'description': f'Đi tới ô hàng xóm ({next_x},{next_y}) và đánh dấu là đã thăm'
                })
                
            else:  # Nếu không có hàng xóm chưa thăm, backtrack
                # Đánh dấu ô hiện tại là backtrack
                cell_types[cell_x][cell_y] = 'backtrack'
                
                # Lưu trạng thái: Đang quay lui
                self.detailed_steps.append({
                    'maze_state': copy.deepcopy(self.maze),
                    'cell_types': copy.deepcopy(cell_types),
                    'algorithm_state': {
                        'stack': copy.deepcopy(stack),
                        'visited': copy.deepcopy(visited)
                    },
                    'description': f'Không có hàng xóm chưa thăm, quay lui từ ô ({x},{y})'
                })
                
                # Quay lui - triển khai giống maze.py
                stack.pop()
                
                if stack:  # Nếu stack không rỗng
                    # Đánh dấu ô mới ở đỉnh stack là current
                    backtrack_x, backtrack_y = stack[-1]
                    cell_types[2*backtrack_x + 1][2*backtrack_y + 1] = 'current'
    
    def _prim_maze_detailed(self):
        """
        Tạo mê cung sử dụng thuật toán Prim và ghi lại chi tiết từng bước
        - Phiên bản này đã điều chỉnh để khớp chính xác với triển khai trong maze.py
        """
        width = 2*self.size + 1
        height = 2*self.size + 1
        
        # Khởi tạo cell_types để theo dõi trạng thái của từng ô
        cell_types = np.full((height, width), 'wall', dtype=object)
        
        # Chọn một ô bắt đầu ngẫu nhiên - giống hệt maze.py
        start_x = random.randrange(1, height, 2)
        start_y = random.randrange(1, width, 2)
        self.maze[start_x][start_y] = 0
        cell_types[start_x][start_y] = 'visited'
        
        # Lưu trạng thái ban đầu
        self.detailed_steps.append({
            'maze_state': copy.deepcopy(self.maze),
            'cell_types': copy.deepcopy(cell_types),
            'algorithm_state': {},
            'description': 'Bắt đầu thuật toán Prim với một ô ngẫu nhiên'
        })
        
        # Danh sách các tường kề với các ô đã thăm - giống hệt maze.py
        walls = []
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            nx, ny = start_x+dx, start_y+dy
            if 1 <= nx < height-1 and 1 <= ny < width-1:
                # Thêm vào danh sách walls theo định dạng (wall_x, wall_y, cell_x, cell_y)
                walls.append((start_x+dx//2, start_y+dy//2, nx, ny))
                cell_types[nx][ny] = 'frontier'
                cell_types[start_x+dx//2][start_y+dy//2] = 'frontier'
        
        # Lưu trạng thái: Sau khi thêm các tường vào danh sách
        self.detailed_steps.append({
            'maze_state': copy.deepcopy(self.maze),
            'cell_types': copy.deepcopy(cell_types),
            'algorithm_state': {
                'walls': copy.deepcopy(walls)
            },
            'description': f'Thêm {len(walls)} tường kề vào danh sách xem xét'
        })
        
        # Lặp cho đến khi không còn tường nào để xem xét - giống maze.py
        while walls:
            # Chọn một tường ngẫu nhiên rồi xóa khỏi danh sách - giống hệt cách làm trong maze.py
            wall_idx = random.randrange(len(walls))
            wx, wy, nx, ny = walls.pop(wall_idx)
            
            # Đánh dấu tường đang xét
            cell_types[wx][wy] = 'current'
            
            # Lưu trạng thái: Đang xem xét tường
            self.detailed_steps.append({
                'maze_state': copy.deepcopy(self.maze),
                'cell_types': copy.deepcopy(cell_types),
                'algorithm_state': {
                    'walls': copy.deepcopy(walls),
                    'current_wall': (wx, wy),
                    'target_cell': (nx, ny)
                },
                'description': f'Đang xem xét tường tại ({wx},{wy}) kết nối với ô ({nx},{ny})'
            })
            
            # Nếu ô kề với tường chưa được thăm
            if self.maze[nx][ny] == 1:
                # Đánh dấu tường và ô mới là đường đi
                self.maze[wx][wy] = 0
                self.maze[nx][ny] = 0
                cell_types[wx][wy] = 'passage'
                cell_types[nx][ny] = 'visited'
                
                # Lưu trạng thái: Đã xóa tường và đánh dấu ô mới
                self.detailed_steps.append({
                    'maze_state': copy.deepcopy(self.maze),
                    'cell_types': copy.deepcopy(cell_types),
                    'algorithm_state': {
                        'walls': copy.deepcopy(walls)
                    },
                    'description': f'Xóa tường và thêm ô ({nx},{ny}) vào mê cung'
                })
                
                # Thêm các tường kề với ô mới vào danh sách - triển khai giống maze.py
                for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
                    nnx, nny = nx+dx, ny+dy
                    if 1 <= nnx < height-1 and 1 <= nny < width-1:
                        if self.maze[nnx][nny] == 1:  # Chỉ thêm nếu ô chưa thuộc mê cung
                            nwx, nwy = nx+dx//2, ny+dy//2
                            walls.append((nwx, nwy, nnx, nny))
                            cell_types[nnx][nny] = 'frontier'
                            cell_types[nwx][nwy] = 'frontier'
                            
                            # Lưu trạng thái mỗi khi thêm tường mới (tùy chọn)
                            self.detailed_steps.append({
                                'maze_state': copy.deepcopy(self.maze),
                                'cell_types': copy.deepcopy(cell_types),
                                'algorithm_state': {
                                    'walls': copy.deepcopy(walls),
                                    'new_wall': (nwx, nwy, nnx, nny)
                                },
                                'description': f'Thêm tường ({nwx},{nwy}) vào danh sách xem xét'
                            })
            else:
                # Nếu ô đã được thăm, đánh dấu tường đã xem xét
                cell_types[wx][wy] = 'wall'
                
                # Lưu trạng thái: Bỏ qua tường này vì ô đã là một phần của mê cung
                self.detailed_steps.append({
                    'maze_state': copy.deepcopy(self.maze),
                    'cell_types': copy.deepcopy(cell_types),
                    'algorithm_state': {
                        'walls': copy.deepcopy(walls)
                    },
                    'description': f'Bỏ qua tường này vì ô ({nx},{ny}) đã thuộc mê cung'
                })
    
    def get_detailed_steps(self):
        """
        Trả về danh sách chi tiết các bước tạo mê cung
        """
        return self.detailed_steps


def create_3blue1brown_animation(algorithm="dfs_backtrack", maze_size=5, interval=500, save_animation=True, show_plot=True):
    """
    Tạo animation phong cách 3Blue1Brown để minh họa quá trình tạo mê cung
    
    Args:
        algorithm: Thuật toán tạo mê cung ("dfs_backtrack" hoặc "prim")
        maze_size: Kích thước mê cung (nên chọn nhỏ để dễ theo dõi, 5-10 là phù hợp)
        interval: Thời gian giữa các frame (ms)
        save_animation: Có lưu animation thành file không
        show_plot: Có hiển thị animation không
    """
    # Tạo mê cung và lấy các bước chi tiết
    print(f"Đang tạo mê cung chi tiết bằng thuật toán {algorithm}...")
    maze = MazeWithDetailedSteps(maze_size, algorithm=algorithm)
    detailed_steps = maze.get_detailed_steps()
    
    print(f"Tạo animation với {len(detailed_steps)} bước...")
    
    # Tạo figure với layout tối ưu cho trình chiếu
    fig = plt.figure(figsize=(12, 8), facecolor=COLORS['background'])
    gs = GridSpec(1, 2, width_ratios=[2, 1], figure=fig)
    
    # Trục bên trái: Hiển thị mê cung
    ax_maze = fig.add_subplot(gs[0])
    ax_maze.set_facecolor(COLORS['background'])
    
    # Trục bên phải: Hiển thị thông tin thuật toán
    ax_info = fig.add_subplot(gs[1])
    ax_info.set_facecolor(COLORS['background'])
    ax_info.axis('off')
    
    # Tiêu đề animation
    title = f"Quá trình tạo mê cung bằng thuật toán {algorithm}"
    fig.suptitle(title, color=COLORS['text'], fontsize=16)
    
    # Tạo bản đồ màu cho các loại ô
    color_map = {
        'wall': COLORS['wall'],
        'passage': COLORS['passage'],
        'current': COLORS['current'],
        'visited': COLORS['visited'],
        'backtrack': COLORS['backtrack'],
        'frontier': COLORS['frontier'],
        'start': COLORS['start'],
        'end': COLORS['end']
    }
    
    # Hàm initialization cho animation
    def init():
        ax_maze.clear()
        ax_maze.set_facecolor(COLORS['background'])
        ax_maze.set_xticks([])
        ax_maze.set_yticks([])
        ax_info.clear()
        ax_info.set_facecolor(COLORS['background'])
        ax_info.axis('off')
        return []
    
    # Hàm update cho animation
    def update(frame):
        # Xóa các trục
        ax_maze.clear()
        ax_info.clear()
        ax_info.axis('off')
        
        # Lấy dữ liệu cho frame hiện tại
        step_data = detailed_steps[frame]
        cell_types = step_data['cell_types']
        description = step_data['description']
        
        # Tạo ma trận màu cho mê cung
        height, width = cell_types.shape
        rgb_data = np.zeros((height, width, 3))
        
        for i in range(height):
            for j in range(width):
                cell_type = cell_types[i, j]
                color = mcolors.to_rgb(color_map.get(cell_type, COLORS['wall']))
                rgb_data[i, j] = color
        
        # Hiển thị mê cung với màu sắc
        ax_maze.imshow(rgb_data)
        
        # Thêm lưới để dễ nhìn hơn
        for i in range(height + 1):
            ax_maze.axhline(i - 0.5, color=COLORS['grid'], linewidth=0.5)
        for j in range(width + 1):
            ax_maze.axvline(j - 0.5, color=COLORS['grid'], linewidth=0.5)
        
        # Thiết lập tên trục
        ax_maze.set_title(f"Bước {frame+1}/{len(detailed_steps)}", color=COLORS['text'])
        ax_maze.set_xticks([])
        ax_maze.set_yticks([])
        
        # Hiển thị thông tin thuật toán
        ax_info.text(0.5, 0.9, "Thuật toán", ha='center', color=COLORS['text'], fontsize=14)
        
        # Mô tả bước hiện tại
        ax_info.text(0.1, 0.8, description, color=COLORS['text'], fontsize=12, 
                    wrap=True, va='top')
        
        # Hiển thị chú thích màu sắc
        y_pos = 0.5
        ax_info.text(0.1, y_pos, "Chú thích:", color=COLORS['text'], fontsize=12)
        y_pos -= 0.05
        
        for label, color_key in [
            ('Tường', 'wall'),
            ('Đường đi', 'passage'),
            ('Ô hiện tại', 'current'),
            ('Ô đã thăm', 'visited'),
            ('Ô quay lui', 'backtrack'),
            ('Ô hàng xóm', 'frontier'),
            ('Điểm bắt đầu', 'start'),
            ('Điểm kết thúc', 'end')
        ]:
            y_pos -= 0.05
            ax_info.add_patch(patches.Rectangle((0.1, y_pos), 0.05, 0.03, 
                                              facecolor=color_map[color_key]))
            ax_info.text(0.2, y_pos, label, color=COLORS['text'], fontsize=10, va='center')
        
    
        
        # Thêm thông tin khác từ trạng thái thuật toán nếu có
        algorithm_state = step_data['algorithm_state']
       
        
        return []
    
    # Tạo animation
    ani = FuncAnimation(fig, update, frames=len(detailed_steps), init_func=init, 
                       blit=True, interval=interval, repeat=True)
    
    # Lưu animation
    if save_animation:
        if not os.path.exists("results"):
            os.makedirs("results")
        
        filename = f"results/3blue1brown_{algorithm}_maze.mp4"
        print(f"Đang lưu animation vào file {filename}...")
        
        # Lưu với chất lượng cao
        ani.save(filename, writer='ffmpeg', fps=24, dpi=200,
                extra_args=['-vcodec', 'libx264'])
        
        print(f"Đã lưu animation thành công!")
    
    # Hiển thị animation
    if show_plot:
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.show()
    else:
        plt.close()


def compare_maze_algorithms():
    """
    So sánh hai thuật toán tạo mê cung bằng cách hiển thị animation song song
    """
    print("\nSo sánh hai thuật toán tạo mê cung với animation phong cách 3Blue1Brown")
    
    # Tạo hai animation riêng biệt
    create_3blue1brown_animation("dfs_backtrack", maze_size=5, interval=500, 
                                save_animation=True, show_plot=True)
    
    create_3blue1brown_animation("prim", maze_size=5, interval=500, 
                                save_animation=True, show_plot=True)


if __name__ == "__main__":
    # Hiển thị menu để người dùng chọn
    print("\nAnimation tạo mê cung phong cách 3Blue1Brown")
    print("1. Animation chi tiết cho DFS Backtracker")
    print("2. Animation chi tiết cho Prim")
    print("3. So sánh hai thuật toán")
    
    choice = input("\nNhập lựa chọn của bạn (1-3): ")
    
    if choice == "1":
        create_3blue1brown_animation("dfs_backtrack", maze_size=5)
    elif choice == "2":
        create_3blue1brown_animation("prim", maze_size=5)
    elif choice == "3":
        compare_maze_algorithms()
    else:
        print("Lựa chọn không hợp lệ!")