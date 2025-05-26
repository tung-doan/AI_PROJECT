import tkinter as tk
from tkinter import ttk, messagebox, Scale
import sys
import os

# Constants
WINDOW_SIZE = "800x800"
COLORS = {
    'bg_primary': '#0f172a',  # Nền chính (xám đậm)
    'bg_secondary': '#1e293b',  # Nền phụ (xám nhẹ hơn)
    'bg_tertiary': '#334155',  # Nền cho combobox/thanh trượt
    'accent_primary': '#2ecc71',  # Xanh lá chính
    'accent_active': '#219653',  # Xanh lá đậm (khi nhấn)
    'text_primary': '#ffffff',  # Văn bản chính
    'text_secondary': '#94a3b8',  # Văn bản phụ
    'success': '#27ae60',  # Màu thành công
    'warning': '#f59e0b'  # Màu cảnh báo
}
FONTS = {
    'title': ('Inter', 20, 'bold'),  # Font tiêu đề
    'label': ('Inter', 12),  # Font nhãn
    'description': ('Inter', 10),  # Font mô tả
    'status': ('Inter', 10, 'italic')  # Font trạng thái
}
ALGORITHMS = [
    ("BFS (Breadth-First)", "BFS", "📊 Đảm bảo đường ngắn nhất"),
    ("DFS (Depth-First)", "DFS", "🔍 Tiết kiệm bộ nhớ"),
    ("A* (A-Star)", "A*", "🌟 Tối ưu & Nhanh")
]

try:
    from maze.maze import Maze
    from animation.A_STAR_animation import create_astar_animation
    from animation.bfs_animation import create_bfs_animation
    from animation.dfs_animation import create_dfs_animation
except ImportError as e:
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    try:
        from maze.maze import Maze
        from animation.A_STAR_animation import create_astar_animation
        from animation.bfs_animation import create_bfs_animation
        from animation.dfs_animation import create_dfs_animation
    except ImportError as final_e:
        messagebox.showerror("Lỗi Nhập", f"Không thể nhập module: {final_e}\nHãy đảm bảo app.py nằm trong thư mục gốc và các tệp cần thiết (maze/maze.py, animation/*.py) được cấu trúc đúng.")
        sys.exit(1)

class ModernMazeApp:
    def __init__(self, root_window):
        self.root_window = root_window
        self._setup_window()
        self._configure_styles()
        self._create_ui_components()

    def _setup_window(self):
        """Thiết lập thuộc tính cửa sổ chính"""
        self.root_window.title("🔍 Trình Mô Phỏng Tìm Đường Mê Cung")
        self.root_window.geometry(WINDOW_SIZE)
        self.root_window.configure(bg=COLORS['bg_primary'])
        self.root_window.resizable(True, True)
        
        # Căn giữa cửa sổ
        self.root_window.update_idletasks()
        x = (self.root_window.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root_window.winfo_screenheight() // 2) - (700 // 2)
        self.root_window.geometry(f"{WINDOW_SIZE}+{x}+{y}")

    def _configure_styles(self):
        """Cấu hình các kiểu giao diện hiện đại"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self._configure_frame_styles()
        self._configure_button_styles()
        self._configure_radiobutton_styles()
        self._configure_label_styles()
        self._configure_combobox_styles()

    def _configure_frame_styles(self):
        """Cấu hình kiểu cho khung và khung nhãn"""
        self.style.configure("Modern.TFrame", 
                           background=COLORS['bg_primary'],
                           relief="flat",
                           borderwidth=0)
        
        self.style.configure("Card.TLabelframe", 
                           background=COLORS['bg_secondary'],
                           relief="solid",
                           borderwidth=1,
                           bordercolor=COLORS['bg_tertiary'])
        
        self.style.configure("Card.TLabelframe.Label", 
                           font=FONTS['label'],
                           background=COLORS['bg_secondary'],
                           foreground=COLORS['accent_primary'])

    def _configure_button_styles(self):
        """Cấu hình kiểu cho nút"""
        self.style.configure("Primary.TButton",
                           font=FONTS['label'],
                           background=COLORS['accent_primary'],
                           foreground=COLORS['text_primary'],
                           borderwidth=0,
                           focuscolor="none",
                           relief="flat",
                           padding=(20, 12))
        
        self.style.map("Primary.TButton",
                     background=[('active', COLORS['accent_active']), ('pressed', COLORS['accent_active'])],
                     foreground=[('active', COLORS['text_primary']), ('pressed', COLORS['text_primary'])])

    def _configure_radiobutton_styles(self):
        """Cấu hình kiểu cho nút radio"""
        self.style.configure("Modern.TRadiobutton",
                           font=FONTS['label'],
                           background=COLORS['bg_secondary'],
                           foreground=COLORS['text_primary'],
                           focuscolor="none",
                           borderwidth=0)
        
        self.style.map("Modern.TRadiobutton",
                     background=[('active', COLORS['bg_tertiary'])],
                     indicatorcolor=[('selected', COLORS['accent_primary'])])

    def _configure_label_styles(self):
        """Cấu hình kiểu cho nhãn"""
        self.style.configure("Modern.TLabel",
                           font=FONTS['description'],
                           background=COLORS['bg_secondary'],
                           foreground=COLORS['text_secondary'])
        
        self.style.configure("Title.TLabel",
                           font=FONTS['title'],
                           background=COLORS['bg_primary'],
                           foreground=COLORS['text_primary'])
        
        self.style.configure("Status.TLabel",
                           font=FONTS['status'],
                           background=COLORS['bg_primary'],
                           foreground=COLORS['text_secondary'])

    def _configure_combobox_styles(self):
        """Cấu hình kiểu cho combobox"""
        self.style.configure("Modern.TCombobox",
                           fieldbackground=COLORS['bg_tertiary'],
                           background=COLORS['accent_primary'],  
                           foreground=COLORS['text_primary'],
                           borderwidth=2,
                           relief="flat",
                           padding=5)  
        
        self.style.map("Modern.TCombobox",
                     fieldbackground=[('readonly', COLORS['bg_tertiary'])],
                     selectbackground=[('readonly', COLORS['bg_tertiary'])],
                     selectforeground=[('readonly', COLORS['text_primary'])],
                     background=[('active', COLORS['accent_active'])])

    def _create_ui_components(self):
        """Tạo các thành phần giao diện"""
        self.main_frame = ttk.Frame(self.root_window, style="Modern.TFrame", padding=30)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self._create_header()
        self._create_controls()
        self._create_action_section()

    def _create_header(self):
        """Tạo phần tiêu đề"""
        header_frame = ttk.Frame(self.main_frame, style="Modern.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 40))
        
        title_label = ttk.Label(header_frame,
                              text="🚀 Mê Cung Tìm Đường",
                              style="Title.TLabel")
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame,
                                 text="Công cụ trực quan hóa thuật toán hiện đại",
                                 font=FONTS['description'],
                                 foreground=COLORS['text_secondary'],
                                 background=COLORS['bg_primary'])
        subtitle_label.pack(pady=(8, 0))

    def _create_controls(self):
        """Tạo bảng điều khiển"""
        controls_container = ttk.Frame(self.main_frame, style="Modern.TFrame")
        controls_container.pack(fill=tk.BOTH, expand=True, pady=(0, 30))
        
        self._create_parameters_panel(controls_container)

    def _create_parameters_panel(self, parent):
        """Tạo bảng điều khiển tham số"""
        params_frame = ttk.LabelFrame(parent, text="⚙️ Cấu Hình Mê Cung & Thuật Toán", style="Card.TLabelframe", padding=25)
        params_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=0)
        
        self._create_algorithm_control(params_frame)  # Thêm điều khiển chọn thuật toán
        self._create_size_control(params_frame)
        self._create_speed_control(params_frame)
        self._create_generation_control(params_frame)
        self._create_complexity_control(params_frame)

    def _create_algorithm_control(self, parent):
        """Tạo điều khiển chọn thuật toán dạng combobox"""
        algo_container = ttk.Frame(parent, style="Modern.TFrame")
        algo_container.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(algo_container, text="🎯 Thuật Toán Tìm Đường:", style="Modern.TLabel").pack(anchor="w")
        
        algo_frame = ttk.Frame(algo_container, style="Modern.TFrame")
        algo_frame.pack(fill=tk.X, pady=(4, 0), anchor="w")
        
        self.selected_algorithm_var = tk.StringVar(value="BFS")  # Giá trị ngắn gọn ban đầu
        algo_display_values = [algo[0] for algo in ALGORITHMS]  # Tên hiển thị cho combobox
        
        algo_combo = ttk.Combobox(algo_frame,
                                textvariable=self.selected_algorithm_var,
                                values=algo_display_values,
                                width=20,
                                state="readonly",
                                style="Modern.TCombobox",
                                font=FONTS['description'])
        algo_combo.set("BFS")  # Hiển thị tên đầy đủ trong combobox
        algo_combo.pack(side=tk.LEFT)
        
        def on_algo_change(event):
            selected_display = algo_combo.get()
            for display_name, value, _ in ALGORITHMS:
                if display_name == selected_display:
                    self.selected_algorithm_var.set(value)  # Gán giá trị ngắn gọn (BFS, DFS, A*)
                    break
            # In giá trị để kiểm tra (có thể xóa sau khi debug)
            print(f"Selected algorithm: {self.selected_algorithm_var.get()}")
        algo_combo.bind('<<ComboboxSelected>>', on_algo_change)

    def _create_size_control(self, parent):
        """Tạo điều khiển kích thước mê cung"""
        size_container = ttk.Frame(parent, style="Modern.TFrame")
        size_container.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(size_container, text="📏 Kích Thước Mê Cung:", style="Modern.TLabel").pack(anchor="w")
        
        size_frame = ttk.Frame(size_container, style="Modern.TFrame")
        size_frame.pack(fill=tk.X, pady=(8, 0), anchor="w")  # Căn trái
        
        self.maze_size_var = tk.StringVar(value="20")
        size_values = ["10", "20", "30", "40", "50", "100"]
        
        size_combo = ttk.Combobox(size_frame,
                                textvariable=self.maze_size_var,
                                values=size_values,
                                width=10,  # Giảm chiều rộng để tròn hơn
                                state="readonly",
                                style="Modern.TCombobox",
                                font=FONTS['description'])
        size_combo.pack(side=tk.LEFT)
        
        ttk.Label(size_frame, text="ô", style="Modern.TLabel").pack(side=tk.LEFT, padx=(8, 0))

    def _create_speed_control(self, parent):
        """Tạo điều khiển tốc độ hoạt hình"""
        speed_container = ttk.Frame(parent, style="Modern.TFrame")
        speed_container.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(speed_container, text="⚡ Tốc Độ Hoạt Hình:", style="Modern.TLabel").pack(anchor="w")
        
        speed_frame = ttk.Frame(speed_container, style="Modern.TFrame")
        speed_frame.pack(fill=tk.X, pady=(8, 0))
        
        self.speed_var = tk.IntVar(value=50)
        
        self.speed_slider = Scale(speed_frame,
                                from_=10,
                                to=200,
                                orient=tk.HORIZONTAL,
                                variable=self.speed_var,
                                length=220,
                                showvalue=True,
                                bg=COLORS['bg_secondary'],
                                highlightthickness=0,
                                troughcolor=COLORS['bg_tertiary'],
                                activebackground=COLORS['accent_primary'],
                                font=FONTS['description'],
                                relief=tk.FLAT,
                                bd=0,
                                sliderlength=30,
                                fg=COLORS['text_primary'])
        self.speed_slider.pack(fill=tk.X)
        
        speed_labels_frame = ttk.Frame(speed_frame, style="Modern.TFrame")
        speed_labels_frame.pack(fill=tk.X, pady=(4, 0))
        
        ttk.Label(speed_labels_frame, text="Nhanh", font=FONTS['description'], 
                 foreground=COLORS['success'], background=COLORS['bg_secondary']).pack(side=tk.LEFT)
        ttk.Label(speed_labels_frame, text="Chậm", font=FONTS['description'],
                 foreground=COLORS['warning'], background=COLORS['bg_secondary']).pack(side=tk.RIGHT)

    def _create_generation_control(self, parent):
        """Tạo điều khiển thuật toán tạo mê cung"""
        gen_container = ttk.Frame(parent, style="Modern.TFrame")
        gen_container.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(gen_container, text="🏗️ Thuật Toán Tạo:", style="Modern.TLabel").pack(anchor="w")
        
        gen_frame = ttk.Frame(gen_container, style="Modern.TFrame")
        gen_frame.pack(fill=tk.X, pady=(8, 0), anchor="w")  # Căn trái
        
        self.maze_gen_algo_var = tk.StringVar(value="prim")
        algo_options = [("Thuật Toán Prim", "prim"), ("DFS Backtrack", "dfs_backtrack")]
        
        gen_combo = ttk.Combobox(gen_frame,
                               values=[option[0] for option in algo_options],
                               width=15,  # Giảm chiều rộng để tròn hơn
                               state="readonly",
                               style="Modern.TCombobox",
                               font=FONTS['description'])
        gen_combo.set("Thuật Toán Prim")
        gen_combo.pack(side=tk.LEFT)
        
        def on_gen_algo_change(event):
            selected_display = gen_combo.get()
            for display, value in algo_options:
                if display == selected_display:
                    self.maze_gen_algo_var.set(value)
                    break
        gen_combo.bind('<<ComboboxSelected>>', on_gen_algo_change)

    def _create_complexity_control(self, parent):
        """Tạo điều khiển độ phức tạp"""
        complexity_container = ttk.Frame(parent, style="Modern.TFrame")
        complexity_container.pack(fill=tk.X)
        
        ttk.Label(complexity_container, text="🧩 Độ Phức Tạp:", style="Modern.TLabel").pack(anchor="w")
        
        complexity_frame = ttk.Frame(complexity_container, style="Modern.TFrame")
        complexity_frame.pack(fill=tk.X, pady=(8, 0), anchor="w")  # Căn trái
        
        self.complexity_var = tk.StringVar(value="0.03")
        complexity_options = [
            ("Đơn Giản", "0.01"),
            ("Dễ", "0.02"), 
            ("Trung Bình", "0.03"),
            ("Khó", "0.05"),
            ("Siêu Khó", "0.08"),
            ("Chuyên Gia", "0.15")
        ]
        
        complexity_combo = ttk.Combobox(complexity_frame,
                                      values=[option[0] for option in complexity_options],
                                      width=10,  # Giảm chiều rộng để tròn hơn
                                      state="readonly",
                                      style="Modern.TCombobox",
                                      font=FONTS['description'])
        complexity_combo.set("Trung Bình")
        complexity_combo.pack(side=tk.LEFT)
        
        def on_complexity_change(event):
            selected_display = complexity_combo.get()
            for display, value in complexity_options:
                if display == selected_display:
                    self.complexity_var.set(value)
                    break
        complexity_combo.bind('<<ComboboxSelected>>', on_complexity_change)

    def _create_action_section(self):
        """Tạo phần nút hành động và trạng thái"""
        action_frame = ttk.Frame(self.main_frame, style="Modern.TFrame")
        action_frame.pack(fill=tk.X, pady=(30, 0))
        
        button_container = ttk.Frame(action_frame, style="Modern.TFrame")
        button_container.pack(pady=(0, 30))
        
        self.run_button = ttk.Button(button_container,
                                   text="🚀 Tạo & Trực Quan Hóa",
                                   command=self.run_visualization,
                                   style="Primary.TButton")
        self.run_button.pack()
        
        status_container = ttk.Frame(action_frame, style="Modern.TFrame")
        status_container.pack(fill=tk.X)
        
        self.status_var = tk.StringVar(value="🎯 Sẵn sàng tạo mê cung và trực quan hóa thuật toán")
        self.status_label = ttk.Label(status_container,
                                    textvariable=self.status_var,
                                    style="Status.TLabel",
                                    wraplength=750,
                                    justify='center')
        self.status_label.pack()

    def _validate_inputs(self):
        """Kiểm tra đầu vào người dùng"""
        try:
            size = int(self.maze_size_var.get())
            speed = self.speed_var.get()
            
            if not (5 <= size <= 100):
                messagebox.showerror("❌ Lỗi Đầu Vào", 
                                   "Kích thước mê cung phải từ 5 đến 100 ô.")
                return False
                
            if not (10 <= speed <= 500):
                messagebox.showerror("❌ Lỗi Đầu Vào", 
                                   "Tốc độ hoạt hình phải từ 10 đến 500 ms.")
                return False
                
            return True
            
        except ValueError:
            messagebox.showerror("❌ Lỗi Đầu Vào", 
                               "Vui lòng nhập giá trị số hợp lệ.")
            return False

    def _update_status(self, message, is_error=False):
        """Cập nhật thông báo trạng thái"""
        prefix = "❌" if is_error else "🔄"
        self.status_var.set(f"{prefix} {message}")
        self.root_window.update()

    def run_visualization(self):
        """Chạy tạo mê cung và trực quan hóa"""
        if not self._validate_inputs():
            return
            
        size = int(self.maze_size_var.get())
        speed = self.speed_var.get()
        maze_gen_algo = self.maze_gen_algo_var.get()
        complexity = float(self.complexity_var.get())
        selected_algo = self.selected_algorithm_var.get()
        
        try:
            self.run_button.configure(state="disabled", text="⏳ Đang xử lý...")
            
            self._update_status(f"Đang tạo mê cung {size}×{size} bằng {maze_gen_algo}...")
            
            maze_obj = Maze(size, complexity=complexity, algorithm=maze_gen_algo)
            print(f"✅ Tạo mê cung thành công: {size}×{size}, độ phức tạp: {complexity}")
            
            self._update_status(f"Đang trực quan hóa thuật toán {selected_algo}...")
            
            animation_params = {
                'interval': speed,
                'save_animation': False,
                'show_plot': True
            }
            
            if selected_algo == "A*":
                create_astar_animation(maze_obj, **animation_params)
            elif selected_algo == "BFS": 
                create_bfs_animation(maze_obj, **animation_params)
            elif selected_algo == "DFS":
                create_dfs_animation(maze_obj, **animation_params)
            else:
                raise ValueError(f"Thuật toán không xác định: {selected_algo}")
                
            self._update_status(f"✅ Hoàn thành trực quan hóa {selected_algo}!")
            
        except Exception as e:
            error_msg = f"Lỗi trực quan hóa: {str(e)}"
            print(f"❌ Lỗi: {error_msg}")
            self._update_status(error_msg, is_error=True)
            messagebox.showerror("⚠️ Lỗi Trực Quan Hóa", error_msg)
            
        finally:
            self.run_button.configure(state="normal", text="🚀 Tạo & Trực Quan Hóa")

def main():
    """Điểm vào chính của ứng dụng"""
    root = tk.Tk()
    app = ModernMazeApp(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n👋 Ứng dụng bị đóng bởi người dùng")
    except Exception as e:
        print(f"❌ Lỗi bất ngờ: {e}")
        messagebox.showerror("Lỗi Ứng Dụng", f"Xảy ra lỗi bất ngờ: {e}")

if __name__ == "__main__":
    main()