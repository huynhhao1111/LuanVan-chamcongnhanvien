import tkinter as tk
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
from train import TrackImages
from add_new import draw_ui
from attendance import attendance
from attendance_statistic import attendance_statistic
from view_employees import view_employees

def open_add_new():
    draw_ui()

def open_management():
    management_window = tk.Toplevel()
    management_window.title("Quản Lý Nhân Viên")
    width = 400
    height = 300
    screen_width = management_window.winfo_screenwidth()
    screen_height = management_window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    management_window.geometry(f"{width}x{height}+{x}+{y}")
    management_window.resizable(0, 0)

    label = tk.Label(management_window, text="Chọn chức năng quản lý", font=("Helvetica", 14, "bold"))
    label.pack(pady=20)

    add_new_employee = tk.Button(management_window, text="Thêm mới nhân viên", bg="#28a745", fg="white", font=("Helvetica", 12), command=open_add_new)
    add_new_employee.pack(padx=20, pady=10)

    statistics_button = tk.Button(management_window, text="Thống kê chấm công", bg="#ffc107", fg="black", font=("Helvetica", 12), command=attendance_statistic)
    statistics_button.pack(padx=20, pady=10)
    # Nút để xem thông tin nhân viên
    statistics_button = tk.Button(management_window, text="Xem Thông Tin Nhân Viên", bg="#ffc107", fg="black",
                                  font=("Helvetica", 12), command=view_employees)
    statistics_button.pack(padx=20, pady=10)

    # view_button = tk.Button(window, text="Xem Thông Tin Nhân Viên", bg="#007bff", font=helv24, command=view_employees)
    # view_button.grid(row=3, column=0, sticky='news', padx=(20, 10), pady=(10, 20))


window = tk.Tk()
window.title("CHẤM CÔNG NHÂN VIÊN")
width = 900
height = 550
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)
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
