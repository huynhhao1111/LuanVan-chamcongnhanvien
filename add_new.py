import tkinter as tk
from tkinter import *
from train import TakeImages, TrainAllImages, extract_images_from_video  # Nhập hàm extract_images_from_video
import tkinter.messagebox as msgbox
import tkinter.font as font
import os
import cv2
from tkinter import filedialog


def demo(e1, e2, e3, e4, e5):
    Id = str(e1.get())
    name = str(e2.get())
    age = str(e3.get())
    gender = str(e4.get())
    cr = str(e5.get())
    msg = TakeImages(Id, name, age, gender, cr)


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


def extract_video_images(e1, e2, e3, e4, e5):  # Hàm mới để gọi extract_images_from_video
    Id = str(e1.get())
    name = str(e2.get())
    age = str(e3.get())
    gender = str(e4.get())
    cr = str(e5.get())

    # Gọi hàm extract_images_from_video
    extract_images_from_video(Id, name, age, gender, cr)


def draw_ui():
    master = tk.Tk()
    width = 600
    height = 400
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    master.geometry("%dx%d+%d+%d" % (width, height, x, y))
    master.title("Thêm mới nhân viên")
    helv24 = font.Font(family='Helvetica', size=16, weight=font.BOLD)

    tk.Label(master, text="ID", font=helv24).place(x=150, y=50, anchor="center")
    tk.Label(master, text="Tên", font=helv24).place(x=150, y=100, anchor="center")
    tk.Label(master, text="Tuổi", font=helv24).place(x=150, y=150, anchor="center")
    tk.Label(master, text="Giới tính", font=helv24).place(x=150, y=200, anchor="center")
    tk.Label(master, text="Vị trí", font=helv24).place(x=150, y=250, anchor="center")

    e1 = tk.Entry(master, width=30)
    e2 = tk.Entry(master, width=30)
    e3 = tk.Entry(master, width=30)
    e4 = tk.Entry(master, width=30)
    e5 = tk.Entry(master, width=30)

    e1.place(x=300, y=50, anchor="center", height=20)
    e2.place(x=300, y=100, anchor="center", height=20)
    e3.place(x=300, y=150, anchor="center", height=20)
    e4.place(x=300, y=200, anchor="center", height=20)
    e5.place(x=300, y=250, anchor="center", height=20)

    # tk.Button(master, text="Thêm ảnh có sẵn", bg="#ffbb33", fg='white', font=helv24,
    #           command=lambda: add_existing_images(e1, e2)).place(x=300, y=350, anchor="center")

    tk.Button(master, text="Lấy ảnh", bg="#01a157", fg='white', font=helv24,
              command=lambda: demo(e1, e2, e3, e4, e5)).place(x=200, y=350, anchor="center")

    # Nút mới để lấy hình ảnh từ video
    tk.Button(master, text="Lấy ảnh từ video", bg="#ff5733", fg='white', font=helv24,
              command=lambda: extract_video_images(e1, e2, e3, e4, e5)).place(x=400, y=350, anchor="center")

    tk.Button(master, text="Train ảnh", bg="#00c0ef", fg='white', font=helv24, command=lambda: TrainAllImages("TrainingImage")).place(x=500, y=350)


    master.mainloop()
