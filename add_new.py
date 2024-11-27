import os
import tkinter as tk
from tkinter import font, StringVar, filedialog, messagebox
import cv2
from train import TakeImages, TrainAllImages, extract_images_from_video

def show_message(title, message, message_type="info"):
    window = tk.Toplevel()
    window.title(title)

    # Kích thước cửa sổ
    window_width = 300
    window_height = 150

    # Lấy kích thước màn hình
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Tính toán tọa độ để canh giữa
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)

    # Đặt vị trí cửa sổ
    window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    window.resizable(False, False)

    # Xác định màu sắc biểu tượng dựa trên loại thông báo
    if message_type == "info":
        icon_color = "green"
    elif message_type == "error":
        icon_color = "red"
    elif message_type == "warning":
        icon_color = "orange"
    else:
        icon_color = "blue"

    # Nội dung thông báo
    tk.Label(window, text=title, font=("Arial", 14, "bold"), fg=icon_color).pack(pady=10)
    tk.Label(window, text=message, font=("Arial", 12), wraplength=280).pack(pady=10)
    tk.Button(window, text="Đóng", command=window.destroy).pack(pady=10)

    # Làm cho cửa sổ trở thành cửa sổ con
    window.transient()
    window.grab_release()

def demo(e1, e2, e3, gender_var, position_var, department_var, root):
    Id = str(e1.get()).strip()
    name = str(e2.get()).strip()
    age = str(e3.get()).strip()
    gender = str(gender_var.get())
    position = str(position_var.get())
    department = str(department_var.get())

    # Kiểm tra thông tin bắt buộc
    if not Id:
        show_message("Lỗi", "Vui lòng nhập Mã Nhân Viên.", "error")
        return
    if not name:
        show_message("Lỗi", "Vui lòng nhập Tên Nhân Viên.", "error")
        return
    if not age:
        show_message("Lỗi", "Vui lòng nhập Tuổi.", "error")
        return

    TakeImages(Id, name, age, gender, position, department)


def add_existing_images(e1, e2, root):
    Id = str(e1.get()).strip()
    name = str(e2.get()).strip()

    # Kiểm tra thông tin bắt buộc
    if not Id:
        show_message("Lỗi", "Vui lòng nhập Mã Nhân Viên.", "error")
        return
    if not name:
        show_message("Lỗi", "Vui lòng nhập Tên Nhân Viên.", "error")
        return

    files = filedialog.askopenfilenames(title="Chọn hình ảnh", filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    if not files:
        show_message("Thông báo", "Bạn chưa chọn ảnh nào.", "warning")
        return

    employee_folder = f"TrainingImage/{name}_{Id}"
    os.makedirs(employee_folder, exist_ok=True)

    for image_path in files:
        img = cv2.imread(image_path)
        if img is not None:
            image_name = os.path.basename(image_path)
            save_path = os.path.join(employee_folder, image_name)
            cv2.imwrite(save_path, img)


def extract_video_images(e1, e2, e3, gender_var, position_var, department_var, root):
    Id = str(e1.get()).strip()
    name = str(e2.get()).strip()
    age = str(e3.get()).strip()
    gender = str(gender_var.get())
    position = str(position_var.get())
    department = str(department_var.get())

    # Kiểm tra thông tin bắt buộc
    if not Id:
        show_message("Lỗi", "Vui lòng nhập Mã Nhân Viên.", "error")
        return
    if not name:
        show_message("Lỗi", "Vui lòng nhập Tên Nhân Viên.", "error")
        return
    if not age:
        show_message("Lỗi", "Vui lòng nhập Tuổi.", "error")
        return

    extract_images_from_video(Id, name, age, gender, position, department, root)
    # show_message("Thành công", "Hình ảnh từ video đã được lưu thành công.", "info")
    # draw_ui(root)

import tkinter as tk
from tkinter import font, StringVar

def draw_ui(root):
    # Tạo cửa sổ mới (Toplevel) thay vì Tk()
    new_window = tk.Toplevel(root)
    new_window.title("Thêm mới nhân viên")
    new_window.configure(bg='#f9f9f9')
    width, height = 900, 550
    screen_width, screen_height = new_window.winfo_screenwidth(), new_window.winfo_screenheight()
    x_coordinate, y_coordinate = (screen_width - width) // 2, (screen_height - height) // 2
    new_window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    header_font = font.Font(family='Helvetica', size=20, weight=font.BOLD)
    label_font = font.Font(family='Helvetica', size=14)
    button_font = font.Font(family='Helvetica', size=12)

    # Header
    tk.Label(new_window, text="Thêm Mới Nhân Viên", font=header_font, bg='#f9f9f9', fg="#333333").pack(pady=20)

    # Input frame
    input_frame = tk.Frame(new_window, bg='#f9f9f9')
    input_frame.pack(pady=20)

    labels = ["Mã Nhân Viên", "Tên Nhân Viên", "Tuổi", "Giới Tính", "Chức Vụ", "Phòng Ban"]
    e1, e2, e3 = tk.Entry(input_frame, width=30), tk.Entry(input_frame, width=30), tk.Entry(input_frame, width=30)

    gender_var, position_var, department_var = StringVar(new_window), StringVar(new_window), StringVar(new_window)
    gender_var.set("Nam")
    position_var.set("Nhân viên")
    department_var.set("Marketing")

    inputs = [
        e1,
        e2,
        e3,
        tk.OptionMenu(input_frame, gender_var, "Nam", "Nữ"),
        tk.OptionMenu(input_frame, position_var, "Nhân viên", "Giám đốc", "Trưởng phòng", "Phó phòng"),
        tk.OptionMenu(input_frame, department_var, "Marketing", "Social", "Kỹ thuật", "Hành chính", "Nhân sự", "Biên tập")
    ]

    for i, (label, input_widget) in enumerate(zip(labels, inputs)):
        tk.Label(input_frame, text=label, font=label_font, bg='#f9f9f9', anchor="w").grid(row=i, column=0, padx=20, pady=10, sticky="w")
        input_widget.grid(row=i, column=1, padx=20, pady=10, sticky="ew")

    # Buttons frame
    button_frame = tk.Frame(new_window, bg='#f9f9f9')
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Lấy Ảnh", bg="#01a157", fg="white", font=button_font,
              command=lambda: demo(e1, e2, e3, gender_var, position_var, department_var, root)).grid(row=0, column=0, padx=10)

    tk.Button(button_frame, text="Lấy Ảnh Từ Video", bg="#ff5733", fg="white", font=button_font,
              command=lambda: extract_video_images(e1, e2, e3, gender_var, position_var, department_var, root)).grid(row=0, column=1, padx=10)

    tk.Button(button_frame, text="Train Lại Tất Cả", bg="#00c0ef", fg="white", font=button_font,
              command=lambda: TrainAllImages("TrainingImage")).grid(row=0, column=2, padx=10)

    new_window.mainloop()

