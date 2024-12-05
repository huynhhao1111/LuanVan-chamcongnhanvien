import tkinter as tk
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
from train import TrackImages
from add_new import draw_ui
from attendance import attendance
from attendance_statistic import attendance_statistic
from view_employees import view_employees
from view_leave import view_leaves
# from attendance_salary import attendance_salary
management_window = None  # Biến toàn cục

# Hàm mở giao diện "Thêm mới nhân viên"
# def open_add_new():
#     draw_ui()

# Hàm mở giao diện "Quản lý"
from tkinter import simpledialog, messagebox

# Hàm mở giao diện "Quản lý"
def open_management():
    global management_window

    # Kiểm tra nếu cửa sổ quản lý đã tồn tại
    if management_window and tk.Toplevel.winfo_exists(management_window):
        management_window.focus()
        return

    # Hàm kiểm tra mật khẩu
    def verify_password():
        entered_password = password_entry.get()
        if entered_password == "123456":  # Thay "123456" bằng mật khẩu của bạn
            password_window.destroy()  # Đóng cửa sổ nhập mật khẩu
            show_management_ui()  # Mở giao diện quản lý
        else:
            error_label.config(text="Mật khẩu không đúng. Vui lòng thử lại.", fg="red")

    # Hàm hiển thị giao diện quản lý
    def show_management_ui():
        global management_window
        management_window = tk.Toplevel()
        management_window.title("Quản Lý")
        width, height = 900, 550
        screen_width, screen_height = management_window.winfo_screenwidth(), management_window.winfo_screenheight()
        x, y = (screen_width - width) // 2, (screen_height - height) // 2
        management_window.geometry(f"{width}x{height}+{x}+{y}")
        management_window.resizable(0, 0)

        # Tiêu đề
        label = tk.Label(
            management_window,
            text="Chọn chức năng quản lý",
            font=("Helvetica", 18, "bold")
        )
        label.grid(row=0, column=0, columnspan=2, pady=20)

        # Cấu hình lưới
        for i in range(2):  # 2 hàng
            management_window.grid_rowconfigure(i + 1, weight=1)
        for j in range(2):  # 2 cột
            management_window.grid_columnconfigure(j, weight=1)

        # Nút Thêm mới nhân viên
        add_new_employee = tk.Button(
            management_window,
            text="Thêm mới nhân viên",
            bg="#28a745",
            fg="black",
            font=("Helvetica", 18, "bold"),
            command=lambda: draw_ui(window)
        )
        add_new_employee.grid(row=1, column=0, padx=20, pady=10, sticky="news")

        # Nút Thống kê chấm công
        statistics_button = tk.Button(
            management_window,
            text="Thống kê chấm công",
            bg="#ffc107",
            fg="black",
            font=("Helvetica", 18, "bold"),
            command=attendance_statistic
        )
        statistics_button.grid(row=1, column=1, padx=20, pady=10, sticky="news")

        # Nút Xem thông tin nhân viên
        view_employees_button = tk.Button(
            management_window,
            text="Xem Thông Tin Nhân Viên",
            bg="#007bff",
            fg="black",
            font=("Helvetica", 18, "bold"),
            command=view_employees
        )
        view_employees_button.grid(row=2, column=0, padx=20, pady=10, sticky="news")

        # Nút Xem thông tin nghỉ phép
        view_leaves_button = tk.Button(
            management_window,
            text="Xem Thông Tin Nghỉ Phép",
            bg="#dc3545",
            fg="black",
            font=("Helvetica", 18, "bold"),
            command=view_leaves
        )
        view_leaves_button.grid(row=2, column=1, padx=20, pady=10, sticky="news")
        # Nút Xem thông tin nghỉ phép
        # attendance_salary_button = tk.Button(
        #     management_window,
        #     text="Tính Lương",
        #     bg="#dc3545",
        #     fg="black",
        #     font=("Helvetica", 18, "bold"),
        #     command=attendance_salary
        # )
        # attendance_salary_button.grid(row=2, column=1, padx=20, pady=10, sticky="news")

    # Tạo cửa sổ nhập mật khẩu
    password_window = tk.Toplevel()
    password_window.title("Xác Thực Mật Khẩu")
    password_window.geometry("400x250")
    password_window.resizable(False, False)

    # Căn giữa cửa sổ
    screen_width, screen_height = password_window.winfo_screenwidth(), password_window.winfo_screenheight()
    x, y = (screen_width - 400) // 2, (screen_height - 250) // 2
    password_window.geometry(f"400x250+{x}+{y}")

    # Khung giao diện
    frame = tk.Frame(password_window, bg="#f8f9fa", padx=20, pady=20)
    frame.pack(expand=True, fill="both")

    # Tiêu đề
    title_label = tk.Label(frame, text="Nhập Mật Khẩu", font=("Helvetica", 16, "bold"), bg="#f8f9fa", fg="#343a40")
    title_label.pack(pady=(10, 20))

    # Ô nhập mật khẩu
    password_entry = tk.Entry(frame, show="*", font=("Helvetica", 14), width=30)
    password_entry.pack(pady=(0, 10))
    password_entry.focus()

    # Nút xác nhận
    submit_button = tk.Button(
        frame,
        text="Xác Nhận",
        font=("Helvetica", 12, "bold"),
        bg="#007bff",
        fg="white",
        command=verify_password
    )
    submit_button.pack(pady=(10, 5))

    # Nhãn thông báo lỗi
    error_label = tk.Label(frame, text="", font=("Helvetica", 10), bg="#f8f9fa", fg="red")
    error_label.pack()

    # Nút hủy
    cancel_button = tk.Button(
        frame,
        text="Hủy",
        font=("Helvetica", 12),
        bg="#6c757d",
        fg="white",
        command=password_window.destroy
    )
    cancel_button.pack(pady=(5, 0))


# Cửa sổ chính
window = tk.Tk()
window.title("CHẤM CÔNG NHÂN VIÊN")
width, height = 900, 550
screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
x, y = (screen_width - width) // 2, (screen_height - height) // 2
window.geometry(f"{width}x{height}+{x}+{y}")
window.resizable(0, 0)
window.configure(background='#f0f2f5')

header_frame = Frame(window, bg="#343a40")
header_frame.grid(row=0, column=0, columnspan=4, sticky='news')
header_frame.columnconfigure(0, weight=1)

title = tk.Label(header_frame, text="CHƯƠNG TRÌNH CHẤM CÔNG", bg="#343a40", fg="white", font=("Helvetica", 28, "bold"))
title.grid(row=0, column=0, pady=20)

helv24 = font.Font(family='Helvetica', size=18, weight=font.BOLD)

# Logo
img = ImageTk.PhotoImage(Image.open("user.png").resize((100, 100), Image.LANCZOS))
logo_label = Label(header_frame, image=img, bg="#343a40")
logo_label.grid(row=0, column=1, padx=50, pady=50)

# Nút 1: Chấm công
mark_attendance = tk.Button(window, text="Chấm công", bg="#00c0ef", font=helv24, height=5, width=10, command=TrackImages)
mark_attendance.grid(row=1, column=0, rowspan=2, sticky='news', padx=(20, 10), pady=(20, 10))

# Nút 2: Kiểm tra chấm công
check_attendance = tk.Button(window, text="Kiểm tra chấm công", bg="#d84a38", font=helv24, command=attendance)
check_attendance.grid(row=1, column=1, columnspan=2, sticky='news', padx=(10, 20), pady=(20, 10))

# Nút 3: Quản lý
manage_button = tk.Button(window, text="Quản lý", bg="#007bff", font=helv24, command=open_management)
manage_button.grid(row=2, column=1, columnspan=2, sticky='news', padx=(10, 20), pady=(10, 20))

Grid.rowconfigure(window, 0, weight=1)
Grid.rowconfigure(window, 1, weight=1)
Grid.rowconfigure(window, 2, weight=1)

Grid.columnconfigure(window, 0, weight=1)
Grid.columnconfigure(window, 1, weight=1)
Grid.columnconfigure(window, 2, weight=1)

window.mainloop()
