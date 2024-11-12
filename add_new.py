import tkinter as tk
from tkinter import *
from train import TakeImages, TrainAllImages, extract_images_from_video  # Nhập hàm extract_images_from_video
import tkinter.messagebox as msgbox
import tkinter.font as font
import os
import cv2
from tkinter import filedialog
from tkinter import ttk


def demo(e1, e2, e3, gender_var, position_var, department_var):
    Id = str(e1.get())
    name = str(e2.get())
    age = str(e3.get())
    gender = str(gender_var.get())  # Lấy giá trị giới tính từ gender_var
    position = str(position_var.get())  # Lấy giá trị vị trí từ position_var
    department = str(department_var.get())
    msg = TakeImages(Id, name, age, gender, position, department)


def add_existing_images(e1, e2):
    files = filedialog.askopenfilenames(title="Chọn hình ảnh", filetypes=[("Image Files", "*.jpg *.png *.jpeg")])

    if not files:
        return

    Id = str(e1.get())
    name = str(e2.get())

    # Tạo thư mục cho nhân viên
    employee_folder = f"TrainingImage/{name}_{Id}"
    os.makedirs(employee_folder, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

    for image_path in files:
        img = cv2.imread(image_path)
        if img is not None:
            # Lưu hình ảnh vào thư mục đã tạo
            image_name = os.path.basename(image_path)
            save_path = os.path.join(employee_folder, image_name)  # Lưu vào thư mục nhân viên
            cv2.imwrite(save_path, img)

    msgbox.showinfo("Thông báo", "Hình ảnh đã được lưu thành công.")


def extract_video_images(e1, e2, e3,gender_var , position_var, department_var):  # Hàm mới để gọi extract_images_from_video
    Id = str(e1.get())
    name = str(e2.get())
    age = str(e3.get())
    gender = str(gender_var.get())  # Lấy giá trị giới tính từ gender_var
    position = str(position_var.get())  # Lấy giá trị vị trí từ position_var
    department = str(department_var.get())

    # Gọi hàm extract_images_from_video
    extract_images_from_video(Id, name, age, gender, position, department)


def draw_ui():
    master = tk.Tk()
    width = 900
    height = 550  # Điều chỉnh lại chiều cao để phù hợp với các trường mới
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    master.geometry("%dx%d+%d+%d" % (width, height, x, y))
    master.title("Thêm mới nhân viên")
    helv24 = font.Font(family='Helvetica', size=16, weight=font.BOLD)

    tk.Label(master, text="Mã Nhân Viên", font=helv24).place(x=150, y=50, anchor="center")
    tk.Label(master, text="Tên Nhân Viên", font=helv24).place(x=150, y=100, anchor="center")
    tk.Label(master, text="Tuổi", font=helv24).place(x=150, y=150, anchor="center")
    tk.Label(master, text="Giới tính", font=helv24).place(x=150, y=200, anchor="center")
    tk.Label(master, text="Chức Vụ", font=helv24).place(x=150, y=250, anchor="center")
    tk.Label(master, text="Phòng Ban", font=helv24).place(x=150, y=300, anchor="center")

    e1 = tk.Entry(master, width=30)
    e2 = tk.Entry(master, width=30)
    e3 = tk.Entry(master, width=30)

    # Tạo OptionMenu cho giới tính
    gender_var = StringVar(master)
    gender_var.set("Nam")  # Giá trị mặc định
    gender_menu = tk.OptionMenu(master, gender_var, "Nam", "Nữ")
    gender_menu.config(width=28)  # Điều chỉnh kích thước

    # Tạo OptionMenu cho vị trí
    position_var = StringVar(master)
    position_var.set("Nhân viên")  # Giá trị mặc định
    position_menu = tk.OptionMenu(master, position_var, "Nhân viên", "Giám đốc", "Trưởng phòng", "Phó phòng")
    position_menu.config(width=28)

    # Tạo OptionMenu cho phòng ban
    department_var = StringVar(master)
    department_var.set("Marketing")  # Giá trị mặc định
    department_menu = tk.OptionMenu(master, department_var, "Marketing", "Social", "Kỹ thuật", "Hành chính", "Nhân sự", "Biên tập")
    department_menu.config(width=28)



    e1.place(x=300, y=50, anchor="center", height=20)
    e2.place(x=300, y=100, anchor="center", height=20)
    e3.place(x=300, y=150, anchor="center", height=20)
    gender_menu.place(x=300, y=200, anchor="center", height=20)
    position_menu.place(x=300, y=250, anchor="center", height=20)
    department_menu.place(x=300, y=300, anchor="center", height=20)

    # Button "Lấy ảnh" (kêu gọi hàm demo)
    tk.Button(master, text="Lấy ảnh", bg="#01a157", fg='white', font=helv24,
              command=lambda: demo(e1, e2, e3, gender_var, position_var, department_var)).place(x=200, y=350, anchor="center")

    # Nút lấy ảnh từ video
    tk.Button(master, text="Lấy ảnh từ video", bg="#ff5733", fg='white', font=helv24,
              command=lambda: extract_video_images(e1, e2, e3, gender_var, position_var, department_var)).place(x=400, y=350, anchor="center")

    # Nút Train ảnh
    tk.Button(master, text="Train Lại Tất Cả Dữ Liệu", bg="#00c0ef", fg='white', font=helv24,
              command=lambda: TrainAllImages("TrainingImage")).place(x=500, y=350)

    master.mainloop()