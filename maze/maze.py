import random
import numpy as np
import time
from collections import defaultdict

"""
Maze class
Cách hoạt động:
* Khởi tạo mê cung: tạo một np.array với tất cả phần tử là tường
* Tạo mê cung ngẫu nhiên sử dụng thuật toán 
* Trả về ma trận mê cung

"""

class Maze:
    def __init__(self, size, complexity=0.05, algorithm="dfs_backtrack"):
        """
        Khởi tạo mê cung với kích thước cho trước
        size: int - kích thước của mê cung (size x size)
        complexity: float - độ phức tạp của mê cung, số càng to càng nhiều ngã rẽ (nên để < 0.1)
        algorithm: str - thuật toán tạo mê cung 
        """
        self.size = size
        self.complexity = complexity
        self.algorithm = algorithm
        # Khởi tạo mê cung với toàn bộ là tường (1)
        self.maze = np.ones((1, 1), dtype=int)
        # Thiết lập điểm bắt đầu và kết thúc
        self.start = (1, 1)
        self.end = (2*size - 1, 2*size - 1)
        # Tạo đường dẫn cho quá trình tạo mê cung
        self.generation_path = []
        # Tạo mê cung
        self.generate_maze()
    
    def generate_maze(self):
        """
        Tạo mê cung ngẫu nhiên dựa trên thuật toán đã chọn
        """
        width = 2*self.size + 1
        height = 2*self.size + 1
        self.maze = np.ones((height, width), dtype=int)
        if self.algorithm == "dfs_backtrack":
            self._dfs_backtrack_maze()
        elif self.algorithm == "prim":
            self._prim_maze()
        else:
            self._dfs_backtrack_maze()
        self.start = (1, 1)
        self.end = (2*self.size - 1, 2*self.size - 1)
        self.maze[self.start[0]][self.start[1]] = 0
        self.maze[self.end[0]][self.end[1]] = 0
        if self.complexity > 0:
            self.add_random_paths()
    
    def _dfs_backtrack_maze(self):
        """
        Tạo mê cung sử dụng thuật toán Depth-First Search Recursive Backtracker
        """
        print("\nĐang tạo mê cung bằng thuật toán DFS Backtracker...")
        time_start = time.time()
        
        # Mảng để đánh dấu các ô đã thăm
        visited = np.zeros((self.size, self.size), dtype=bool)
        
        # Chọn một vị trí bắt đầu ngẫu nhiên
        start_x = random.randint(0, self.size-1)
        start_y = random.randint(0, self.size-1)
        
        # Đánh dấu ô bắt đầu đã thăm
        visited[start_x][start_y] = True
        
        # Chuyển đổi tọa độ logic sang tọa độ ma trận
        cell_x = 2*start_x + 1
        cell_y = 2*start_y + 1
        
        # Đánh dấu ô hiện tại là đường đi
        self.maze[cell_x][cell_y] = 0
        
        # Stack để lưu trữ các ô đã thăm để backtracking
        stack = [(start_x, start_y)]
      
        
        # Đếm số ô đã thăm
        visit_counter = 1
        
        # Lặp cho đến khi tất cả các ô đều được thăm
        while visit_counter < self.size * self.size:
            x, y = stack[-1]  # Lấy ô hiện tại từ đỉnh stack
            
            # Tìm tất cả các hàng xóm chưa thăm
            neighbors = []
            for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if 0 <= nx < self.size and 0 <= ny < self.size and not visited[nx][ny]:
                    neighbors.append((nx, ny))
            
            if neighbors:  # Nếu có hàng xóm chưa thăm
                # Chọn một hàng xóm ngẫu nhiên
                next_x, next_y = random.choice(neighbors)
                
                # Đánh dấu hàng xóm đã thăm
                visited[next_x][next_y] = True
                visit_counter += 1
                
                # Xóa tường giữa ô hiện tại và hàng xóm
                wall_x = 2*x + 1 + (next_x - x)
                wall_y = 2*y + 1 + (next_y - y)
                self.maze[wall_x][wall_y] = 0
                
                # Đánh dấu ô hàng xóm là đường đi
                cell_x = 2*next_x + 1
                cell_y = 2*next_y + 1
                self.maze[cell_x][cell_y] = 0
                
                # Thêm hàng xóm vào stack và đường dẫn
                stack.append((next_x, next_y))
            
                
            else:  # Nếu không có hàng xóm chưa thăm, backtrack
                stack.pop()
        print(f"Thời gian thực hiện thuật toán: {time.time() - time_start:.4f}s")

    def _prim_maze(self):
        """
        Tạo mê cung sử dụng thuật toán Prim
        """
        print("\nĐang tạo mê cung bằng thuật toán Prim...")
        time_start = time.time()
        width = 2*self.size + 1
        height = 2*self.size + 1
        self.maze = np.ones((height, width), dtype=int)
        start_x = random.randrange(1, height, 2)
        start_y = random.randrange(1, width, 2)
        self.maze[start_x][start_y] = 0
        walls = []
        # Thêm 4 bức tường vào hàng đợi
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            nx, ny = start_x+dx, start_y+dy
            if 1 <= nx < height-1 and 1 <= ny < width-1:
                walls.append((start_x+dx//2, start_y+dy//2, nx, ny))
        while walls:
            wx, wy, nx, ny = walls.pop(random.randrange(len(walls)))
            if self.maze[nx][ny] == 1:
                self.maze[wx][wy] = 0
                self.maze[nx][ny] = 0
                for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
                    nnx, nny = nx+dx, ny+dy
                    if 1 <= nnx < height-1 and 1 <= nny < width-1:
                        if self.maze[nnx][nny] == 1:
                            walls.append((nx+dx//2, ny+dy//2, nnx, nny))
        print(f"Thời gian thực hiện thuật toán: {time.time() - time_start:.4f}s")

    def add_random_paths(self):
        """
        Thêm một số đường đi ngẫu nhiên để tạo nhiều ngã rẽ hơn
        """
        # Số lượng đường đi ngẫu nhiên muốn thêm vào
        num_extra_paths = int(self.size * self.size * self.complexity)
        
        width = 2*self.size + 1
        height = 2*self.size + 1
        
        # Tìm các bức tường có thể phá để tạo đường đi mới
        walls = []
        for x in range(1, height-1):
            for y in range(1, width-1):
                if self.maze[x][y] == 1:
                    # Chỉ xem xét các tường giữa các ô (không phải tường biên)
                    if ((x % 2 == 1 and y % 2 == 0) or (x % 2 == 0 and y % 2 == 1)):
                        # Đếm số ô đường đi xung quanh
                        path_count = 0
                        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < height and 0 <= ny < width and self.maze[nx][ny] == 0:
                                path_count += 1
                        
                        # Chỉ xem xét các bức tường kết nối hai đường đi
                        if path_count >= 2:
                            walls.append((x, y))
        
        # Phá bỏ một số bức tường ngẫu nhiên để tạo đường đi mới
        random.shuffle(walls)
        for i in range(min(num_extra_paths, len(walls))):
            x, y = walls[i]
            self.maze[x][y] = 0
    
    def get_maze(self):
        """
        Trả về ma trận mê cung
        """
        return self.maze
    
    def print_maze(self):
        """
        In mê cung ra màn hình console
        nếu là 0 thì in ra khoảng trắng, nếu là 1 thì in ra dấu #
        """
        for row in self.maze:
            print(''.join(' ' if cell == 0 else '#' for cell in row))