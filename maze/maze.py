import random
import numpy as np
import time
from collections import defaultdict

class Maze:
    def __init__(self, size, complexity=0.05, algorithm="dfs_backtrack"):
        """
        Khởi tạo mê cung với kích thước cho trước
        size: int - kích thước của mê cung (size x size)
        complexity: float - độ phức tạp của mê cung, số càng to càng nhiều ngã rẽ (nên để < 50)
        algorithm: str - thuật toán tạo mê cung
        """
        self.size = size
        self.complexity = complexity
        self.algorithm = algorithm.lower()
        self.maze = np.ones((1, 1), dtype=int)
        self.start = (1, 1)
        self.end = (2*size - 1, 2*size - 1)
        self.generation_path = []
        self.generate_maze()

    def generate_maze(self):
        """
        Tạo mê cung ngẫu nhiên dựa trên thuật toán đã chọn
        """
        width = 2*self.size + 1
        height = 2*self.size + 1
        self.maze = np.ones((height, width), dtype=int)
        self.generation_path = []
        
        if self.algorithm == "dfs_backtrack":
            self._dfs_backtrack_maze()
        elif self.algorithm == "prim":
            self._prim_maze()
        elif self.algorithm == "kruskal":
            self._kruskal_maze()
        else:
            self._dfs_backtrack_maze()
            
        self.start = (1, 1)
        self.end = (2*self.size - 1, 2*self.size - 1)
        self.maze[self.start[0], self.start[1]] = 0
        self.maze[self.end[0], self.end[1]] = 0
        if self.complexity > 0:
            self.add_random_paths()

    def _dfs_backtrack_maze(self):
            print("\nĐang tạo mê cung bằng thuật toán DFS Backtrack...")
            visited = np.zeros((self.size, self.size), dtype=bool)
            start_x = random.randint(0, self.size-1)
            start_y = random.randint(0, self.size-1)
            visited[start_x, start_y] = True

            cell_x = 2*start_x + 1
            cell_y = 2*start_y + 1
            self.maze[cell_x, cell_y] = 0
            self.generation_path.append(("start_cell", cell_x, cell_y))

            stack = [(start_x, start_y)]
            self.generation_path.append(("push_stack", cell_x, cell_y, stack.copy()))
            visit_counter = 1

            while stack and visit_counter < self.size * self.size:
                x, y = stack[-1]
                neighbors = []
                for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                    if 0 <= nx < self.size and 0 <= ny < self.size and not visited[nx, ny]:
                        neighbors.append((nx, ny))

                if neighbors:
                    # Ghi lại các ô hàng xóm
                    neighbor_cells = [(2*nx + 1, 2*ny + 1) for nx, ny in neighbors]
                    self.generation_path.append(("neighbors", neighbor_cells))

                    next_x, next_y = random.choice(neighbors)
                    visited[next_x, next_y] = True
                    visit_counter += 1

                    # Xóa tường
                    wall_x = 2*x + 1 + (next_x - x)
                    wall_y = 2*y + 1 + (next_y - y)
                    self.maze[wall_x, wall_y] = 0
                    self.generation_path.append(("break_wall", wall_x, wall_y))

                    # Đánh dấu ô mới
                    cell_x = 2*next_x + 1
                    cell_y = 2*next_y + 1
                    self.maze[cell_x, cell_y] = 0
                    self.generation_path.append(("new_cell", cell_x, cell_y))

                    stack.append((next_x, next_y))
                    self.generation_path.append(("push_stack", cell_x, cell_y, stack.copy()))
                else:
                    stack.pop()
                    self.generation_path.append(("pop_stack", x, y, stack.copy()))

    def _prim_maze(self):
        print("\nĐang tạo mê cung bằng thuật toán Prim...")
        width = 2*self.size + 1
        height = 2*self.size + 1
        self.maze = np.ones((height, width), dtype=int)

        start_x = random.randrange(1, height, 2)
        start_y = random.randrange(1, width, 2)
        self.maze[start_x, start_y] = 0
        self.generation_path.append(("start_cell", start_x, start_y))

        walls = []
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nx, ny = start_x + dx, start_y + dy
            if 1 <= nx < height-1 and 1 <= ny < width-1:
                walls.append((start_x + dx//2, start_y + dy//2, nx, ny))
                self.generation_path.append(("wall_candidate", start_x + dx//2, start_y + dy//2, nx, ny))

        visited_cells = {(start_x, start_y)}
        while walls:
            # Ghi lại các ô hàng xóm
            neighbor_cells = [wall[2:] for wall in walls if wall[2:] not in visited_cells]
            self.generation_path.append(("neighbors", neighbor_cells))

            # Chọn bức tường ngẫu nhiên
            wx, wy, nx, ny = walls.pop(random.randrange(len(walls)))
            if self.maze[nx, ny] == 1:
                self.maze[wx, wy] = 0
                self.maze[nx, ny] = 0
                self.generation_path.append(("break_wall", wx, wy))
                self.generation_path.append(("new_cell", nx, ny))
                visited_cells.add((nx, ny))

                # Thêm các bức tường mới xung quanh ô mới
                for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                    nnx, nny = nx + dx, ny + dy
                    if 1 <= nnx < height-1 and 1 <= nny < width-1 and self.maze[nnx, nny] == 1:
                        walls.append((nx + dx//2, ny + dy//2, nnx, nny))
                        self.generation_path.append(("wall_candidate", nx + dx//2, ny + dy//2, nnx, nny))
    
    def _kruskal_maze(self):
        print("\nĐang tạo mê cung bằng thuật toán Kruskal...")
        width = 2*self.size + 1
        height = 2*self.size + 1
        self.maze = np.ones((height, width), dtype=int)
        
        # Đánh dấu các ô cell (vị trí lẻ, lẻ)
        for i in range(1, height, 2):
            for j in range(1, width, 2):
                self.maze[i, j] = 0
                self.generation_path.append(("cell", i, j))
        
        # Chuẩn bị các tập hợp cho Union-Find
        parent = {}
        rank = {}
        
        def make_set(x):
            parent[x] = x
            rank[x] = 0
            
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            if root_x != root_y:
                if rank[root_x] < rank[root_y]:
                    parent[root_x] = root_y
                else:
                    parent[root_y] = root_x
                    if rank[root_x] == rank[root_y]:
                        rank[root_x] += 1
                return True
            return False
        
        # Tạo tập hợp cho mỗi ô
        for i in range(self.size):
            for j in range(self.size):
                cell = (i, j)
                make_set(cell)
        
        # Tạo danh sách các bức tường giữa các ô
        walls = []
        for i in range(self.size):
            for j in range(self.size):
                cell = (i, j)
                cell_x, cell_y = 2*i + 1, 2*j + 1
                
                # Xem xét bức tường phía đông
                if j < self.size - 1:
                    east_cell = (i, j + 1)
                    walls.append((cell, east_cell, cell_x, cell_y + 1))
                
                # Xem xét bức tường phía nam
                if i < self.size - 1:
                    south_cell = (i + 1, j)
                    walls.append((cell, south_cell, cell_x + 1, cell_y))
        
        # Xáo trộn danh sách tường
        random.shuffle(walls)
        
        # Áp dụng thuật toán Kruskal
        for cell1, cell2, wall_x, wall_y in walls:
            # Ghi lại các ô hiện tại (các ô vừa được hợp nhất)
            current_cells = [(2*i + 1, 2*j + 1) for i, j in [cell1, cell2] if find(cell1) != find(cell2)]
            if current_cells:
                self.generation_path.append(("current_cells", current_cells))
            if union(cell1, cell2):
                self.maze[wall_x, wall_y] = 0
                self.generation_path.append(("break_wall", wall_x, wall_y))

    def add_random_paths(self):
        """
        Thêm đường đi ngẫu nhiên để tăng ngã rẽ
        """
        num_extra_paths = int(self.size * self.size * self.complexity)
        width = 2*self.size + 1
        height = 2*self.size + 1

        walls = []
        for x in range(1, height-1):
            for y in range(1, width-1):
                if self.maze[x, y] == 1 and ((x % 2 == 1 and y % 2 == 0) or (x % 2 == 0 and y % 2 == 1)):
                    path_count = sum(1 for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                                     if 0 <= x + dx < height and 0 <= y + dy < width and self.maze[x + dx, y + dy] == 0)
                    if path_count >= 2:
                        walls.append((x, y))

        random.shuffle(walls)
        for i in range(min(num_extra_paths, len(walls))):
            x, y = walls[i]
            self.maze[x, y] = 0
            self.generation_path.append(("wall", x, y))

    def get_maze(self):
        """
        Trả về ma trận mê cung
        """
        return self.maze

    def print_maze(self):
        """
        In mê cung ra console
        """
        for row in self.maze:
            print(''.join(' ' if cell == 0 else '#' for cell in row))