import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import time
import matplotlib.animation as animation

def find_path(maze_obj, return_search_steps=False):
    """
    Tìm đường đi từ điểm bắt đầu đến điểm kết thúc trong mê cung
    sử dụng thuật toán DFS (Depth-First Search)
    
    maze_obj: instance của lớp Maze
    return_search_steps: bool - nếu True, hàm sẽ trả về thêm các bước tìm kiếm
    
    Trả về:
    - path: list các tọa độ (x, y) thể hiện đường đi từ điểm bắt đầu đến điểm kết thúc
           hoặc None nếu không tìm thấy đường đi
    - search_steps: list các tọa độ (x, y) theo thứ tự được thăm (nếu return_search_steps=True)
    """
    maze = maze_obj.maze  # Truy cập ma trận mê cung trực tiếp
    start = maze_obj.start
    end = maze_obj.end
    height, width = maze.shape  # Lấy kích thước từ maze.shape
    
    # Tạo ma trận visited để theo dõi các ô đã thăm với kích thước đúng
    visited = np.zeros((height, width), dtype=bool)
    
    # Tạo ma trận parent để lưu trữ đường đi
    parent = np.zeros((height, width, 2), dtype=int)
    parent.fill(-1)  # Khởi tạo tất cả các giá trị là -1
    
    # Khởi tạo stack cho DFS
    stack = [start]
    visited[start] = True
    
    # Lưu các bước tìm kiếm nếu cần
    search_steps = [start] if return_search_steps else None
    
    # Các hướng có thể di chuyển: lên, phải, xuống, trái
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    # DFS để tìm đường đi
    found = False
    while stack and not found:
        current_x, current_y = stack.pop()
        current = (current_x, current_y) # Define current tuple

        # Thêm vào search_steps nếu cần và không phải là điểm bắt đầu (đã được thêm lúc khởi tạo)
        if return_search_steps and current != start and visited[current_x, current_y]: # Check visited to avoid re-adding if logic changes
             # Check if already added to search_steps to prevent duplicates if a node is pushed multiple times before visiting
            if search_steps[-1] != current: # Simple check, might need more robust for complex scenarios
                search_steps.append(current)

        # Kiểm tra nếu đã đến đích
        if current == end:
            found = True
            break
        
        # Kiểm tra các hướng có thể di chuyển
        for dx, dy in directions:
            next_x, next_y = current_x + dx, current_y + dy
            next_pos = (next_x, next_y)
            
            # Kiểm tra xem ô kế tiếp có hợp lệ không
            if (0 <= next_x < height and 0 <= next_y < width and
                    maze[next_x, next_y] == 0 and not visited[next_x, next_y]):
                stack.append(next_pos)
                visited[next_x, next_y] = True
                parent[next_x, next_y] = [current_x, current_y]


    # Tái tạo đường đi nếu tìm thấy
    if found:
        path = []
        curr = end # Use a different variable name to avoid conflict
        while curr != start and curr[0] != -1:
            path.append(curr)
            curr_x, curr_y = curr
            parent_x, parent_y = parent[curr_x, curr_y]
            curr = (parent_x, parent_y)
            if parent_x == -1 or parent_y == -1: # Avoid infinite loop if start is not reachable
                break
        path.append(start)
        path.reverse()
        
        if return_search_steps:
            return path, search_steps
        return path
    else:
        if return_search_steps:
            # Ensure search_steps is returned even if no path is found
            return None, search_steps if search_steps else [] 
        return None

def print_maze_with_path(maze_obj, path):
    """
    In mê cung ra màn hình console với đường đi được biểu diễn bằng '-'
    
    maze_obj: instance của lớp Maze
    path: list các tọa độ (x, y) thể hiện đường đi
    """
    if path is None:
        print("Không tìm thấy đường đi!")
        return
        
    maze_display = maze_obj.maze.copy() # Use a different name to avoid confusion
    
    # Đánh dấu đường đi bằng giá trị 2
    for x, y in path:
        maze_display[x, y] = 2 # Use the copied maze
    
    # In mê cung với đường đi
    for row in maze_display: # Use the copied maze
        print(''.join('#' if cell == 1 else '-' if cell == 2 else ' ' for cell in row))

def visualize_maze_with_path(maze_obj, path):
    """
    Trực quan hóa mê cung với đường đi được đánh dấu
    
    maze_obj: instance của lớp Maze
    path: list các tọa độ (x, y) thể hiện đường đi
    """
    if path is None:
        print("Không tìm thấy đường đi để hiển thị!")
        # Optionally, still display the maze
        # maze = maze_obj.maze
        # height, width = maze.shape
        # fig, ax = plt.subplots(figsize=(10, 10))
        # ax.set_facecolor('white')
        # for i in range(height):
        #     for j in range(width):
        #         if maze[i, j] == 1:
        #             rect = Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor='navy', edgecolor='navy')
        #             ax.add_patch(rect)
        # start = maze_obj.start
        # end = maze_obj.end
        # ax.plot(start[1], start[0], 'go', markersize=8)
        # ax.plot(end[1], end[0], 'bo', markersize=8)
        # ax.set_xlim(-0.5, width - 0.5)
        # ax.set_ylim(-0.5, height - 0.5)
        # ax.set_xticks([])
        # ax.set_yticks([])
        # ax.invert_yaxis()
        # ax.set_aspect('equal')
        # plt.title('Maze (No Path Found)')
        # plt.tight_layout()
        # plt.show()
        return
        
    maze = maze_obj.maze
    height, width = maze.shape
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_facecolor('white')
    
    for i in range(height):
        for j in range(width):
            if maze[i, j] == 1:
                rect = Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor='navy', edgecolor='navy')
                ax.add_patch(rect)
    
    if path:
        path_x = [y for x, y in path]
        path_y = [x for x, y in path]
        ax.plot(path_x, path_y, 'r-', linewidth=2)
        ax.plot(path_x, path_y, 'ro', markersize=3)
    
    start = maze_obj.start
    end = maze_obj.end
    ax.plot(start[1], start[0], 'go', markersize=8, label='Start')
    ax.plot(end[1], end[0], 'bo', markersize=8, label='End')
    
    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(-0.5, height - 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.invert_yaxis()
    ax.set_aspect('equal')
    plt.title('Maze Solution (DFS)')
    plt.legend()
    plt.tight_layout()
    plt.show()

def visualize_search_process(maze_obj, speed=100):
    """
    Hiển thị quá trình tìm kiếm DFS trong mê cung qua animation
    
    maze_obj: instance của lớp Maze
    speed: số millisecond cho mỗi bước animation (càng nhỏ càng nhanh)
    """
    path, search_steps = find_path(maze_obj, return_search_steps=True)
    
    if not search_steps: # Handle case where find_path might return None for search_steps
        print("No search steps to visualize.")
        if path: # If path found but no steps (should not happen with current find_path)
             visualize_maze_with_path(maze_obj,path)
        else: # No path and no steps
             visualize_maze_with_path(maze_obj,None) # Show empty maze
        return

    maze = maze_obj.maze
    height, width = maze.shape
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_facecolor('white')
    
    for i in range(height):
        for j in range(width):
            if maze[i, j] == 1:
                rect = Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor='navy', edgecolor='navy')
                ax.add_patch(rect)
    
    start_node = maze_obj.start # Renamed to avoid conflict
    end_node = maze_obj.end     # Renamed to avoid conflict
    ax.plot(start_node[1], start_node[0], 'go', markersize=8)
    ax.plot(end_node[1], end_node[0], 'bo', markersize=8)
    
    # For DFS, "frontier" is the stack, "explored" are visited nodes not in stack.
    # "current" is the node being popped from stack.
    # We will simplify:
    # - 'yo' (yellow) for nodes that have been visited (popped from stack and processed)
    # - 'mo' (magenta) for the current node being processed
    # - 'co' (cyan) for nodes currently in the stack (the frontier) - this is harder to show accurately with DFS's LIFO
    # For simplicity, we'll show 'search_steps' as they are explored.
    
    explored_plot, = ax.plot([], [], 'yo', markersize=4, alpha=0.4) # Nodes visited
    current_plot, = ax.plot([], [], 'mo', markersize=7, alpha=0.8) # Current node from search_steps
    path_plot, = ax.plot([], [], 'r-', linewidth=2)
    path_markers, = ax.plot([], [], 'ro', markersize=4)
    
    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(-0.5, height - 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.invert_yaxis()
    ax.set_aspect('equal')
    
    title = ax.set_title('Tìm kiếm DFS: Bước 0')
    
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='g', markersize=8, label='Điểm bắt đầu'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='b', markersize=8, label='Điểm kết thúc'),
        # plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='c', markersize=8, label='Trong Stack (Frontier)'), # Hard to show for DFS simply
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='m', markersize=8, label='Đang xét'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='y', markersize=8, label='Đã xét'),
        plt.Line2D([0], [0], color='r', label='Đường đi')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize='small')
    
    def init():
        current_plot.set_data([], [])
        explored_plot.set_data([], [])
        path_plot.set_data([], [])
        path_markers.set_data([], [])
        title.set_text('Tìm kiếm DFS: Bước 0')
        return current_plot, explored_plot, path_plot, path_markers, title
    
    def update(frame):
        # `search_steps` for DFS records the order nodes are popped from the stack (explored).
        if frame < len(search_steps):
            current_cell = search_steps[frame]
            current_plot.set_data([current_cell[1]], [current_cell[0]])
            
            if frame > 0:
                # All previous steps are "explored"
                explored_y = [y for x, y in search_steps[:frame]]
                explored_x = [x for x, y in search_steps[:frame]]
                explored_plot.set_data(explored_y, explored_x)
            else:
                explored_plot.set_data([], []) # Clear explored at the first frame if current is start
                # If start is the first in search_steps, current_plot will show it.
            
            title.set_text(f'Tìm kiếm DFS: Bước {frame+1}/{len(search_steps)}')
  
            path_plot.set_data([], [])
            path_markers.set_data([], [])

        else: # After all search steps are shown, display the final path
            current_plot.set_data([], []) # Clear current node
            # Keep explored nodes visible
            if search_steps:
                 explored_y = [y for x,y in search_steps]
                 explored_x = [x for x,y in search_steps]
                 explored_plot.set_data(explored_y, explored_x)

            if path:
                path_y = [y for x, y in path]
                path_x = [x for x, y in path]
                path_plot.set_data(path_y, path_x)
                path_markers.set_data(path_y, path_x)
                title.set_text(f'Đường đi DFS: {len(path)} bước')
            else:
                title.set_text('Không tìm thấy đường đi (DFS)!')
        
        return current_plot, explored_plot, path_plot, path_markers, title

    # Number of frames for animation
    # One frame for each step in search_steps, then a few more to display the path clearly.
    num_frames = len(search_steps)
    if path:
        num_frames += 10 # Extra frames to show the path

    anim = animation.FuncAnimation(fig, update, frames=num_frames, 
                                   init_func=init, blit=True, interval=speed, repeat=False)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Import lớp Maze từ module maze
    from maze.maze import Maze
    
    # Tạo mê cung mới
    maze = Maze(10, complexity=0.03, algorithm="dfs_backtrack")
    
    # In mê cung ban đầu
    print("Mê cung ban đầu:")
    maze.print_maze()
    print("\n")
    
    # Chọn chế độ hiển thị
    show_animation = True  # Đặt thành True để xem animation, False để chỉ xem kết quả cuối cùng
    
    if show_animation:
        # Hiển thị quá trình tìm kiếm với animation
        visualize_search_process(maze, speed=100)  # speed càng nhỏ càng nhanh
    else:
        # Tìm đường đi và hiển thị kết quả cuối cùng
        start_time = time.time()
        path = find_path(maze)
        end_time = time.time()
        
        if path:
            print(f"Tìm thấy đường đi với {len(path)} bước:")
            print(f"Độ dài đường đi: {len(path) - 1}")  # Trừ 1 vì đường đi bao gồm cả nút bắt đầu
            print(f"Thời gian thực thi: {end_time - start_time:.5f} giây")
            print_maze_with_path(maze, path)
            visualize_maze_with_path(maze, path)
        else:
            print("Không tìm thấy đường đi!")
            print(f"Thời gian thực thi: {end_time - start_time:.5f} giây")