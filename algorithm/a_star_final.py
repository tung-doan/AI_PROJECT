import numpy as np
import heapq
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import time
import matplotlib.animation as animation

def manhattan_distance(p1, p2):
    """
    Tính khoảng cách Manhattan giữa hai điểm
    
    p1, p2: tuple (x, y) biểu diễn tọa độ các điểm
    
    Trả về: khoảng cách Manhattan giữa p1 và p2
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_path(maze_obj, return_search_steps=False):
    """
    Tìm đường đi từ điểm bắt đầu đến điểm kết thúc trong mê cung
    sử dụng thuật toán A* với heuristic là Manhattan Distance
    
    maze_obj: instance của lớp Maze
    return_search_steps: bool - nếu True, hàm sẽ trả về thêm các bước tìm kiếm
    
    Trả về:
    - path: list các tọa độ (x, y) thể hiện đường đi từ điểm bắt đầu đến điểm kết thúc
           hoặc None nếu không tìm thấy đường đi
    - search_steps: list các tọa độ (x, y) theo thứ tự được thăm (nếu return_search_steps=True)
    - frontier_history: list các list tọa độ (x, y) thể hiện frontier tại mỗi bước (nếu return_search_steps=True)
    """
    maze = maze_obj.maze  
    start = maze_obj.start
    end = maze_obj.end
    height, width = maze.shape  
    
    # Tạo ma trận visited để theo dõi các ô đã thăm
    visited = np.zeros((height, width), dtype=bool)
    
    # Tạo ma trận parent để lưu trữ đường đi
    parent = np.zeros((height, width, 2), dtype=int)
    parent.fill(-1)  # Khởi tạo tất cả các giá trị là -1
    
    # Tạo ma trận g_score để lưu trữ chi phí từ điểm bắt đầu đến mỗi ô
    g_score = np.full((height, width), np.inf)
    g_score[start] = 0
    
    # Tạo ma trận f_score để lưu trữ chi phí ước tính từ mỗi ô đến đích
    f_score = np.full((height, width), np.inf)
    f_score[start] = manhattan_distance(start, end)
    
    # Khởi tạo hàng đợi ưu tiên cho A*
    # Mỗi phần tử trong hàng đợi là (f_score, g_score, vị trí)
    # Sử dụng g_score trong trường hợp f_score bằng nhau
    # Ưu tiên xét điểm gần điểm xuất phát hơn
    # Thêm biến đếm để tránh so sánh vị trí khi f_score và g_score bằng nhau
    # Nếu hai điểm có f_score và g_score bằng nhau, điểm nào có score nhỏ hơn xét trc
    count = 0
    open_set = [(f_score[start], 0, count, start)]
    heapq.heapify(open_set)
    
    # Các hướng có thể di chuyển: lên, phải, xuống, trái
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    # Lưu các bước tìm kiếm và lịch sử frontier
    search_steps = [start] if return_search_steps else None
    frontier_history = [[start]] if return_search_steps else None
    
    # A* để tìm đường đi
    found = False
    while open_set and not found:
        # Lấy node có f_score thấp nhất từ hàng đợi ưu tiên
        _, _, _, current = heapq.heappop(open_set)
        current_x, current_y = current
        
        # Nếu đã thăm node này rồi, bỏ qua
        if visited[current_x, current_y]:
            continue
            
        # Đánh dấu đã thăm
        visited[current_x, current_y] = True
        
        # Thêm vào search_steps
        if return_search_steps and current != start:
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
                
                # Tính toán g_score mới (chi phí từ start đến next_pos qua current)
                tentative_g_score = g_score[current_x, current_y] + 1
                
                # Nếu tìm thấy đường đi tốt hơn đến next_pos
                if tentative_g_score < g_score[next_x, next_y]:
                    # Cập nhật parent
                    parent[next_x, next_y] = [current_x, current_y]
                    
                    # Cập nhật g_score và f_score
                    g_score[next_x, next_y] = tentative_g_score
                    f_score[next_x, next_y] = tentative_g_score + manhattan_distance(next_pos, end)
                    
                    # Thêm vào hàng đợi ưu tiên
                    count += 1
                    heapq.heappush(open_set, (f_score[next_x, next_y], tentative_g_score, count, next_pos))
        
        # Lưu trạng thái frontier sau mỗi bước
        if return_search_steps:
            # Chuyển đổi open_set thành list các tọa độ
            current_frontier = [pos for _, _, _, pos in open_set]
            frontier_history.append(current_frontier)
    
    # Tái tạo đường đi nếu tìm thấy
    if found:
        path = []
        current = end
        while current != start:
            path.append(current)
            current_x, current_y = current
            parent_x, parent_y = parent[current_x, current_y]
            current = (parent_x, parent_y)
            
        path.append(start)
        path.reverse()  # Đảo ngược để có đường đi từ start đến end
        
        if return_search_steps:
            return path, search_steps, frontier_history
        return path
    else:
        if return_search_steps:
            return None, search_steps, frontier_history
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
        
    maze = maze_obj.maze.copy()
    
    # Đánh dấu đường đi bằng giá trị 2
    for x, y in path:
        maze[x, y] = 2
    
    # In mê cung với đường đi
    for row in maze:
        print(''.join('#' if cell == 1 else '-' if cell == 2 else ' ' for cell in row))

def visualize_maze_with_path(maze_obj, path):
    """
    Trực quan hóa mê cung với đường đi được đánh dấu
    Đường đi sẽ đi qua tâm của mỗi ô
    
    maze_obj: instance của lớp Maze
    path: list các tọa độ (x, y) thể hiện đường đi
    """
    if path is None:
        print("Không tìm thấy đường đi để hiển thị!")
        return
        
    maze = maze_obj.maze
    height, width = maze.shape
    
    # Tạo hình vẽ
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Vẽ nền trắng cho toàn bộ mê cung
    ax.set_facecolor('white')
    
    # Duyệt qua tất cả các ô trong mê cung
    for i in range(height):
        for j in range(width):
            if maze[i, j] == 1:  # Nếu là tường
                # Tạo hình chữ nhật tô đặc
                rect = Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor='navy', edgecolor='navy')
                ax.add_patch(rect)
    
    # Vẽ đường đi
    if path:
        # Chuyển đổi tọa độ cho đường đi
        path_x = [y for x, y in path]
        path_y = [x for x, y in path]
        
        # Vẽ đường đi
        ax.plot(path_x, path_y, 'r-', linewidth=2)
        
        # Vẽ điểm tròn ở mỗi ô trên đường đi
        ax.plot(path_x, path_y, 'ro', markersize=3)
    
    # Đánh dấu điểm bắt đầu và kết thúc
    start = maze_obj.start
    end = maze_obj.end
    ax.plot(start[1], start[0], 'go', markersize=8)
    ax.plot(end[1], end[0], 'bo', markersize=8)
    
    # Thiết lập giới hạn trục
    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(-0.5, height - 0.5)
    
    # Ẩn các trục
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Đảo ngược trục y để phù hợp với hiển thị mê cung
    ax.invert_yaxis()
    
    # Thiết lập tỷ lệ bằng nhau trên cả hai trục
    ax.set_aspect('equal')
    
    plt.title('Maze Solution (A* with Manhattan Distance)')
    plt.tight_layout()
    plt.show()

def visualize_search_process(maze_obj, speed=100):
    """
    Hiển thị quá trình tìm kiếm A* trong mê cung qua animation
    
    maze_obj: instance của lớp Maze
    speed: số millisecond cho mỗi bước animation (càng nhỏ càng nhanh)
    """
    path, search_steps, frontier_history = find_path(maze_obj, return_search_steps=True)
    
    maze = maze_obj.maze
    height, width = maze.shape
    
    # Tạo hình vẽ
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Vẽ nền trắng cho toàn bộ mê cung
    ax.set_facecolor('white')
    
    # Duyệt qua tất cả các ô trong mê cung
    for i in range(height):
        for j in range(width):
            if maze[i, j] == 1:  # Nếu là tường
                # Tạo hình chữ nhật tô đặc
                rect = Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor='navy', edgecolor='navy')
                ax.add_patch(rect)
    
    # Đánh dấu điểm bắt đầu và kết thúc
    start = maze_obj.start
    end = maze_obj.end
    ax.plot(start[1], start[0], 'go', markersize=8)
    ax.plot(end[1], end[0], 'bo', markersize=8)
    
    # Khởi tạo plot rỗng cho vùng đã thăm (frontier)
    frontier_plot, = ax.plot([], [], 'co', markersize=6, alpha=0.6)
    
    # Khởi tạo plot rỗng cho vùng đang thăm hiện tại
    current_plot, = ax.plot([], [], 'mo', markersize=7, alpha=0.8)
    
    # Khởi tạo plot rỗng cho vùng đã thăm xong (explored)
    explored_plot, = ax.plot([], [], 'yo', markersize=4, alpha=0.4)
    
    # Khởi tạo plot rỗng cho đường đi
    path_plot, = ax.plot([], [], 'r-', linewidth=2)
    path_markers, = ax.plot([], [], 'ro', markersize=4)
    
    # Thiết lập giới hạn trục
    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(-0.5, height - 0.5)
    
    # Ẩn các trục
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Đảo ngược trục y để phù hợp với hiển thị mê cung
    ax.invert_yaxis()
    
    # Thiết lập tỷ lệ bằng nhau trên cả hai trục
    ax.set_aspect('equal')
    
    # Tạo tiêu đề với thông tin
    title = ax.set_title('Tìm kiếm A*: Bước 0')
    
    # Thêm chú thích
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='g', markersize=8, label='Điểm bắt đầu'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='b', markersize=8, label='Điểm kết thúc'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='c', markersize=8, label='Đang trong hàng đợi'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='m', markersize=8, label='Đang xét'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='y', markersize=8, label='Đã xét'),
        plt.Line2D([0], [0], color='r', label='Đường đi')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize='small')
    
    def init():
        frontier_plot.set_data([], [])
        current_plot.set_data([], [])
        explored_plot.set_data([], [])
        path_plot.set_data([], [])
        path_markers.set_data([], [])
        title.set_text('Tìm kiếm A*: Bước 0')
        return frontier_plot, current_plot, explored_plot, path_plot, path_markers, title
    
    # Tính toán tổng số frame: số bước tìm kiếm + số bước hiển thị đường đi
    total_exploration_frames = len(search_steps)
    total_path_frames = len(path) if path else 0
    # Thêm một vài frame chuyển tiếp giữa quá trình thăm và hiển thị đường đi
    transition_frames = 5
    total_frames = total_exploration_frames + transition_frames + total_path_frames
    
    def update(frame):
        # Phân chia quá trình animation thành hai giai đoạn: thăm và hiển thị đường đi
        if frame < total_exploration_frames:
            # Giai đoạn 1: Hiển thị quá trình thăm
            
            # Ô hiện tại đang xét (màu tím)
            if frame > 0:
                current_cell = search_steps[frame]
                current_plot.set_data([current_cell[1]], [current_cell[0]])
            else:
                current_plot.set_data([], [])
                
            # Các ô đã xét xong (màu vàng)
            if frame > 1:
                explored_y = [y for x, y in search_steps[:frame-1]]
                explored_x = [x for x, y in search_steps[:frame-1]]
                explored_plot.set_data(explored_y, explored_x)
            else:
                explored_plot.set_data([], [])
                
            # Các ô trong frontier - nằm trong hàng đợi (màu xanh)
            if frame < len(frontier_history):
                current_frontier = frontier_history[frame]
                if current_frontier:
                    frontier_y = [y for x, y in current_frontier]
                    frontier_x = [x for x, y in current_frontier]
                    frontier_plot.set_data(frontier_y, frontier_x)
                else:
                    frontier_plot.set_data([], [])
            else:
                frontier_plot.set_data([], [])
                
            # Hiển thị số lượng ô trong frontier
            frontier_count = len(frontier_history[frame]) if frame < len(frontier_history) else 0
            title.set_text(f'Tìm kiếm A*: Bước {frame+1}/{total_exploration_frames} - Frontier: {frontier_count} ô')
            
            # Không hiển thị đường đi trong giai đoạn này
            path_plot.set_data([], [])
            path_markers.set_data([], [])
            
        elif frame < total_exploration_frames + transition_frames:
            # Giai đoạn chuyển tiếp: giữ nguyên trạng thái cuối cùng của quá trình thăm
            # nhưng thay đổi tiêu đề để chuẩn bị cho hiển thị đường đi
            transition_step = frame - total_exploration_frames + 1
            
            # Hiển thị tất cả các ô đã thăm
            if search_steps:
                explored_y = [y for x, y in search_steps]
                explored_x = [x for x, y in search_steps]
                explored_plot.set_data(explored_y, explored_x)
            
            # Xóa hiển thị ô hiện tại và frontier khi chuyển sang giai đoạn tiếp theo
            current_plot.set_data([], [])
            frontier_plot.set_data([], [])
            
            # Thay đổi tiêu đề trong giai đoạn chuyển tiếp
            title.set_text(f'Hoàn thành tìm kiếm! Chuẩn bị hiển thị đường đi ({transition_step}/{transition_frames})')
            
            # Vẫn chưa hiển thị đường đi
            path_plot.set_data([], [])
            path_markers.set_data([], [])
            
        else:
            # Giai đoạn 2: Hiển thị đường đi
            # Đã thăm hết tất cả các ô, bây giờ hiển thị đường đi từng bước một
            
            # Tính số bước đường đi cần hiển thị trong frame hiện tại
            path_frame = frame - (total_exploration_frames + transition_frames)
            path_steps = min(path_frame + 1, total_path_frames)
            
            if path and path_steps > 0:
                # Hiển thị đường đi dần dần từ xuất phát đến đích
                path_y = [y for x, y in path[:path_steps]]
                path_x = [x for x, y in path[:path_steps]]
                path_plot.set_data(path_y, path_x)
                path_markers.set_data(path_y, path_x)
                
                title.set_text(f'Hiển thị đường đi: {path_steps}/{total_path_frames} bước')
            else:
                title.set_text('Không tìm thấy đường đi!')
                
            # Vẫn giữ nguyên hiển thị các ô đã thăm
            if search_steps:
                explored_y = [y for x, y in search_steps]
                explored_x = [x for x, y in search_steps]
                explored_plot.set_data(explored_y, explored_x)
            
            # Không hiển thị ô hiện tại và frontier trong giai đoạn này
            current_plot.set_data([], [])
            frontier_plot.set_data([], [])
            
        return frontier_plot, current_plot, explored_plot, path_plot, path_markers, title
    
    # Tạo animation
    anim = animation.FuncAnimation(fig, update, frames=total_frames, 
                                   init_func=init, blit=True, interval=speed)
    
    plt.tight_layout()
    plt.show()

def find_path_and_visualize(maze_obj, show_animation=False, speed=100):
    """
    Tìm đường đi trong mê cung sử dụng A* và hiển thị kết quả
    
    maze_obj: instance của lớp Maze
    show_animation: bool - nếu True, hiển thị animation quá trình tìm kiếm
    speed: số millisecond cho mỗi bước animation (càng nhỏ càng nhanh)
    """
    if show_animation:
        print("\nHiển thị quá trình tìm kiếm A*...")
        visualize_search_process(maze_obj, speed)
        return
    
    print("\nĐang tìm đường đi bằng thuật toán A*...")
    start_time = time.time()
    path = find_path(maze_obj)
    end_time = time.time()
    
    if path is not None:
        print(f"Tìm thấy đường đi với {len(path)} bước:")
        print(f"Độ dài đường đi: {len(path) - 1}")
        print(f"Thời gian thực thi: {end_time - start_time:.5f} giây")
        visualize_maze_with_path(maze_obj, path)
    else:
        print("Không tìm thấy đường đi trong mê cung!")
        print(f"Thời gian thực thi: {end_time - start_time:.5f} giây")
        # Hiển thị mê cung mà không có đường đi
        visualize_maze_with_path(maze_obj, [])

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Import lớp Maze từ module maze
    from maze.maze import Maze
    
    # Tạo mê cung mới
    maze = Maze(5, complexity=0.03, algorithm="dfs_backtrack")
    
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