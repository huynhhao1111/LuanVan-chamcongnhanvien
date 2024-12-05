import tkinter as tk
from tkinter import filedialog
from tkinter import Message, Text
from tkinter.font import names

import cv2, os
import shutil
import csv
import pickle

import face_recognition
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
import tkinter.messagebox as msgbox
from csv import DictWriter
import sqlite3
from tempfile import NamedTemporaryFile
import shutil
# Hàm hiển thị thông báo sử dụng Toplevel
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
import tkinter as tk
import unicodedata

def remove_accent(text):
    text = unicodedata.normalize('NFD', text)  # Chuẩn hóa Unicode dạng NFD
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')  # Loại bỏ dấu
    return text
def ask_yes_no(title, message):
    """
    Tạo một cửa sổ hỏi xác nhận (Yes/No) với thiết kế đẹp hơn.
    :param title: Tiêu đề của cửa sổ.
    :param message: Nội dung câu hỏi.
    :return: True nếu chọn "Yes", False nếu chọn "No".
    """
    result = {"value": None}

    def on_yes():
        result["value"] = "yes"
        confirm_window.destroy()

    def on_no():
        result["value"] = "no"
        confirm_window.destroy()

    # Tạo cửa sổ Toplevel
    confirm_window = tk.Toplevel()
    confirm_window.title(title)

    # Kích thước cửa sổ
    window_width = 350
    window_height = 200

    # Lấy kích thước màn hình
    screen_width = confirm_window.winfo_screenwidth()
    screen_height = confirm_window.winfo_screenheight()

    # Tính toán tọa độ để canh giữa
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)

    # Đặt vị trí và kích thước cửa sổ
    confirm_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    confirm_window.resizable(False, False)
    confirm_window.grab_set()  # Chặn thao tác bên ngoài cửa sổ này

    # Tạo nền và thêm viền
    confirm_window.configure(bg="#f0f8ff")  # Màu nền nhạt (AliceBlue)

    # Tiêu đề thông báo
    tk.Label(
        confirm_window,
        text=title,
        font=("Arial", 14, "bold"),
        fg="#2f4f4f",  # Màu chữ (Dark Slate Gray)
        bg="#f0f8ff",
        pady=10
    ).pack()

    # Nội dung thông báo
    tk.Label(
        confirm_window,
        text=message,
        font=("Arial", 12),
        wraplength=320,
        fg="#333333",  # Màu chữ (Gray)
        bg="#f0f8ff",
        padx=20,
        pady=10
    ).pack()

    # Khung nút bấm
    button_frame = tk.Frame(confirm_window, bg="#f0f8ff")
    button_frame.pack(pady=20)

    # Nút "Có" (Yes)
    tk.Button(
        button_frame,
        text="Có",
        width=12,
        bg="#32cd32",  # Màu xanh lá (Lime Green)
        fg="white",
        font=("Arial", 10, "bold"),
        command=on_yes
    ).grid(row=0, column=0, padx=10)

    # Nút "Không" (No)
    tk.Button(
        button_frame,
        text="Không",
        width=12,
        bg="#dc143c",  # Màu đỏ (Crimson)
        fg="white",
        font=("Arial", 10, "bold"),
        command=on_no
    ).grid(row=0, column=1, padx=10)

    # Chờ cửa sổ đóng và trả kết quả
    confirm_window.wait_window()
    return result["value"]

def show_message_and_wait(title, message, master=None):
    # Tạo cửa sổ pop-up
    popup = tk.Toplevel(master)
    popup.title(title)
    popup.geometry("300x150")
    popup.resizable(False, False)

    # Căn giữa cửa sổ
    window_width = 300
    window_height = 150
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)
    popup.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Hiển thị nội dung thông báo
    tk.Label(popup, text=title, font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(popup, text=message, font=("Arial", 12), wraplength=280).pack(pady=10)

    # Nút xác nhận
    tk.Button(popup, text="Xác nhận", command=popup.destroy).pack(pady=10)

    # Chặn luồng chính cho đến khi cửa sổ pop-up đóng
    popup.transient(master)  # Đảm bảo pop-up ở trên cửa sổ chính
    popup.grab_set()  # Chặn tương tác bên ngoài pop-up
    popup.wait_window()

def is_valid_id(Id):
    return Id.isdigit() and len(Id) == 5

# Hàm kiểm tra tên chỉ chứa chữ cái
def is_valid_name(name):
    return name.isalpha()

# Hàm kiểm tra dữ liệu
def validate_data(Id, name):
    errors = []  # Danh sách chứa các lỗi

    # Kiểm tra ID
    if not is_valid_id(Id):
        errors.append("ID phải là 5 chữ số.")

    conn = sqlite3.connect("FaceBaseNew.db")
    cursor = conn.execute('SELECT * FROM People WHERE ID=' + str(Id))
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
        break

        # Cập nhật hoặc chèn bản ghi
    if isRecordExist == 1:
        errors.append(f"ID {Id} đã tồn tại. Vui lòng nhập ID khác.")

    # # Kiểm tra tên
    # if not is_valid_name(name):
    #     errors.append("Tên chỉ chứa chữ cái.")

    # Trả về danh sách lỗi nếu có, ngược lại trả về None
    if errors:
        return errors
    else:
        return None
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# set text style
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (0, 255, 0)
fontcolor1 = (0, 0, 255)

from unidecode import unidecode

# Hàm xử lý tên để loại bỏ dấu và thay thế khoảng trắng
def format_name(name):
    # Loại bỏ dấu và thay thế khoảng trắng bằng dấu gạch dưới
    formatted_name = unidecode(name).replace(" ", "_")
    return formatted_name

# Cập nhật lại hàm TakeImages
def TakeImages(Id, name, age, gender, cr, pb, root):
    validation_errors = validate_data(Id, name)
    if validation_errors:
        for error in validation_errors:
            # msgbox.showerror("Lỗi", error)
            show_message("Lỗi",error, error)
        return False
    if not validation_errors:
        insertOrUpdate(Id, name, age, gender, cr, pb)
        cam = cv2.VideoCapture(0)
        cam.set(3, 1920)
        cam.set(4, 1080)

        sampleNum = 0

        # Xử lý tên người dùng
        formatted_name = format_name(name)

        # Tạo thư mục theo tên của người dùng và ID
        folder_name = f"TrainingImage/{formatted_name}_{Id}"
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name)  # Xóa toàn bộ ảnh cũ
        os.makedirs(folder_name)  # Tạo lại thư mục mới

        while True:
            ret, frame = cam.read()
            if not ret:
                print("Không thể truy cập webcam!")
                break

            cv2.putText(frame, f'Sample: {sampleNum}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow('frame', frame)

            if sampleNum < 70:
                # Lưu ảnh vào thư mục
                image_path = os.path.join(folder_name, f"{formatted_name}_{Id}_{sampleNum + 1}.jpg")
                cv2.imwrite(image_path, frame)
                print(f"Lưu ảnh: {image_path}")

                sampleNum += 1

                time.sleep(0.2)

            if sampleNum >= 70:
                print("Đã chụp đủ 70 ảnh.")
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()

        user_choice = ask_yes_no("Thông báo", "Bạn đã lấy đủ ảnh. Tiến hành lấy dữ liệu khuôn mặt? Chọn 'Yes' để lấy dữ liệu hoặc 'No' để lấy lại hình ảnh.")
        if user_choice == 'yes':
            TrainImages(folder_name, f"{formatted_name}_{Id}", root)
            # show_message("Thông báo", f"Dữ liệu khuôn mặt của bạn đã được mã hóa và lưu vào file encodings.pickle với ID: {Id}, Name: {formatted_name}")
            # msgbox.showinfo("Thông báo", f"Dữ liệu khuôn mặt của bạn đã được mã hóa và lưu vào file encodings.pickle với ID: {Id}, Name: {formatted_name}")
        else:
            print("Mở lại webcam để lấy lại hình ảnh...")
            TakeImages(Id, name, age, gender, cr, root)  # Gọi lại hàm để lấy lại hình ảnh

# Cập nhật lại hàm extract_images_from_video
import threading


def extract_images_from_video(Id, name, age, gender, cr, pb, root):
    validation_errors = validate_data(Id, name)
    if validation_errors:
        for error in validation_errors:
            show_message("Lỗi", error, error)
        return False

    if not validation_errors:
        insertOrUpdate(Id, name, age, gender, cr, pb)
        video_path = filedialog.askopenfilename(title="Chọn video",
                                                filetypes=[("Video Files", "*.mp4 *.avi *.mov")])

        if not video_path:
            return
        formatted_name = format_name(name)
        folder_name = f"TrainingImage/{formatted_name}_{Id}"
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name)
        os.makedirs(folder_name)

        cap = cv2.VideoCapture(video_path)
        sampleNum = 0
        last_capture_time = time.time()
        capture_complete = False  # Flag để kiểm tra khi nào chụp đủ ảnh

        # Lấy thông tin màn hình và video
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Tính toán kích thước khung hình dọc phù hợp
        # aspect_ratio = video_height / video_width
        window_height = 680  # Chiều cao tối đa 80% màn hình
        window_width = 520
        # if window_width > screen_width * 0.8:  # Nếu chiều rộng quá lớn, điều chỉnh lại
        #     window_width = int(screen_width * 0.8)
        #     window_height = int(window_width * aspect_ratio)

        # Tính toán vị trí trung tâm
        window_x = (screen_width - window_width) // 2
        window_y = (screen_height - window_height) // 2

        # Tạo cửa sổ phụ (Toplevel)
        top = tk.Toplevel(root)
        top.title("Video Capture")
        top.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

        canvas = tk.Canvas(top, width=window_width, height=window_height)
        canvas.pack()

        def update_frame():
            nonlocal sampleNum, last_capture_time, capture_complete

            ret, frame = cap.read()
            if not ret:
                print("Không thể đọc khung hình từ video!")
                cap.release()
                cv2.destroyAllWindows()
                return

            current_time = time.time()
            if current_time - last_capture_time >= 0.1:
                sampleNum += 1

                image_path = os.path.join(folder_name, f"{formatted_name}_{Id}_{sampleNum}.jpg")
                cv2.imwrite(image_path, frame)

                last_capture_time = current_time
                cv2.putText(frame, f'Sample: {sampleNum}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # Chuyển frame thành ảnh cho Tkinter
                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img_rgb)
                img_tk = ImageTk.PhotoImage(img_pil)

                # Cập nhật ảnh lên canvas
                canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)
                canvas.image = img_tk  # Giữ tham chiếu đến ảnh

            if sampleNum >= 70 and not capture_complete:
                capture_complete = True  # Đánh dấu quá trình chụp ảnh đã hoàn tất
                print("Đã chụp đủ 70 ảnh.")
                cap.release()
                cv2.destroyAllWindows()
                top.destroy()

                # Gọi hàm để hiển thị thông báo và bắt đầu quá trình huấn luyện
                # show_message("Thông báo", "Đã chụp đủ 70 ảnh. Tiến hành huấn luyện!", "info")
                top.after(100, ask_user_and_train)  # Sử dụng after để thực hiện sau khi đóng video

            top.after(50, update_frame)  # Cập nhật sau mỗi 50ms

        def ask_user_and_train():
            user_choice = ask_yes_no("Thông báo", "Bạn đã lấy đủ ảnh. Tiến hành lấy dữ liệu khuôn mặt? Chọn 'Yes' để lấy dữ liệu hoặc 'No' để lấy lại hình ảnh.")
            if user_choice == 'yes':
                TrainImages(folder_name, f"{formatted_name}_{Id}", root)
                # show_message("Thông báo", f"Dữ liệu khuôn mặt của bạn đã được mã hóa ID: {Id}, Tên Nhân Viên: {formatted_name}", "info")
            else:
                print("Mở lại video để lấy lại hình ảnh...")
                extract_images_from_video(Id, name, age, gender, cr, pb, root)  # Gọi lại hàm để lấy lại hình ảnh

        update_frame()  # Bắt đầu vòng lặp cập nhật hình ảnh


def insertOrUpdate(id, name, age, gender, cr, pb):
    conn = sqlite3.connect("FaceBaseNew.db")
    cursor = conn.execute('SELECT * FROM People WHERE ID=' + str(id))
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
        break

    # Cập nhật hoặc chèn bản ghi
    if isRecordExist == 1:
        cmd = f"UPDATE People SET Name='{str(name)}', Age='{str(age)}', Gender='{str(gender)}', CR='{str(cr)}', phong_ban='{str(pb)}' WHERE ID={str(id)}"
    else:
        cmd = f"INSERT INTO People(ID, Name, Age, Gender, CR, phong_ban) VALUES({str(id)}, '{str(name)}', '{str(age)}', '{str(gender)}', '{str(cr)}', '{str(pb)}')"

    # Thực thi câu lệnh SQL
    conn.execute(cmd)
    conn.commit()
    conn.close()



import tkinter as tk
from tkinter import Toplevel, Label
import threading
import os
import cv2
import pickle
import face_recognition

import threading
import os
import pickle
import cv2
import face_recognition
from tkinter import Toplevel, Label, messagebox

def TrainImages(training_dir, person_name, root):
    # Tạo cửa sổ chờ Toplevel
    wait_window = Toplevel(root)
    wait_window.title("Đang huấn luyện...")
    wait_window.geometry("300x150")
    wait_window.resizable(False, False)

    # Đặt cửa sổ nằm giữa màn hình
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    wait_window.geometry(
        f"+{root_x + root_width // 2 - 150}+{root_y + root_height // 2 - 75}"
    )

    # Nhãn thông báo
    label = Label(wait_window, text="Đang huấn luyện dữ liệu, vui lòng chờ...", font=("Arial", 12))
    label.pack(pady=20)

    # Thanh tiến trình
    progress = ttk.Progressbar(wait_window, mode="indeterminate")
    progress.pack(pady=10)
    progress.start(10)

    def run_training():
        print("[INFO] Bắt đầu huấn luyện...")
        encodings = []
        names = []

        # Tải dữ liệu mã hóa cũ nếu tệp tồn tại
        if os.path.exists("encodings/encodings.pickle"):
            with open("encodings/encodings.pickle", "rb") as f:
                data = pickle.load(f)
                encodings = data.get("encodings", [])
                names = data.get("names", [])

        # Duyệt qua từng file ảnh trong thư mục training_dir
        for image_name in os.listdir(training_dir):
            image_path = os.path.join(training_dir, image_name)

            # Đọc ảnh
            image = cv2.imread(image_path)
            if image is None:
                print(f"[WARNING] Không thể đọc ảnh: {image_path}")
                continue

            # Chuyển đổi ảnh sang RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Nhận diện khuôn mặt và mã hóa
            boxes = face_recognition.face_locations(rgb_image, model="hog")
            encodings_face = face_recognition.face_encodings(rgb_image, boxes)

            # Kiểm tra nếu phát hiện được khuôn mặt
            if len(encodings_face) == 0:
                print(f"[WARNING] Không tìm thấy khuôn mặt trong ảnh: {image_path}")
                continue

            # Lưu mã hóa và tên vào danh sách
            for encoding in encodings_face:
                encodings.append(encoding)
                names.append(person_name)

        # Kiểm tra nếu có mã hóa nào được lưu
        if len(encodings) == 0:
            print("[ERROR] Không có mã hóa nào được lưu, quá trình huấn luyện thất bại.")
            wait_window.destroy()  # Đóng cửa sổ chờ
            return

        # Tạo thư mục lưu encodings nếu chưa tồn tại
        if not os.path.exists("encodings"):
            os.makedirs("encodings")

        # Lưu dữ liệu mã hóa mới vào tệp encodings.pickle
        data = {"encodings": encodings, "names": names}
        with open("encodings/encodings.pickle", "wb") as f:
            f.write(pickle.dumps(data))

        print("[INFO] Đã hoàn thành huấn luyện và lưu mã hóa.")
        wait_window.destroy()  # Đóng cửa sổ chờ khi hoàn thành

        # Hiển thị thông báo khi huấn luyện thành công
        show_message("Huấn luyện hoàn thành", f"Dữ liệu khuôn mặt của bạn đã được huấn luyện thành công và lưu trữ.\nID: {person_name}")

    # Chạy hàm trong một luồng riêng biệt để không làm gián đoạn giao diện người dùng
    threading.Thread(target=run_training).start()


def TrainAllImages(training_dir):
    print("[INFO] bắt đầu huấn luyện...")

    encodings = []
    names = []

    # Duyệt qua tất cả các thư mục con trong thư mục training_dir
    for person_name in os.listdir(training_dir):
        person_path = os.path.join(training_dir, person_name)

        # Kiểm tra xem đó có phải là thư mục không
        if os.path.isdir(person_path):
            # Duyệt qua từng file ảnh trong thư mục của nhân viên
            for image_name in os.listdir(person_path):
                image_path = os.path.join(person_path, image_name)

                # Đọc ảnh
                image = cv2.imread(image_path)
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Nhận diện khuôn mặt và mã hóa
                boxes = face_recognition.face_locations(rgb_image, model="hog")
                encodings_face = face_recognition.face_encodings(rgb_image, boxes)

                # Lưu mã hóa và tên vào danh sách
                for encoding in encodings_face:
                    encodings.append(encoding)
                    names.append(person_name)

    # Lưu dữ liệu mã hóa vào file encodings.pickle
    if not os.path.exists("encodings"):
        os.makedirs("encodings")
    data = {"encodings": encodings, "names": names}
    with open("encodings/encodings.pickle", "wb") as f:
        f.write(pickle.dumps(data))

    print("[INFO] đã hoàn thành huấn luyện và lưu mã hóa.")





def getImagesAndLabels(path):
    faces = []
    Ids = []
    unique_ids = set()  # Tập hợp để lưu ID duy nhất

    for person_dir in os.listdir(path):
        person_path = os.path.join(path, person_dir)
        if '_' in person_dir:  # Kiểm tra định dạng
            name, Id = person_dir.split('_')
            Id = int(Id)  # Chuyển ID sang số nguyên
            unique_ids.add(Id)  # Thêm ID vào tập hợp

            for image_name in os.listdir(person_path):
                if image_name.endswith(".jpg") or image_name.endswith(".png"):
                    image_path = os.path.join(person_path, image_name)
                    # Sử dụng OpenCV để đọc ảnh
                    image_np = cv2.imread(image_path)

                    # Chuyển đổi từ BGR sang RGB
                    rgb_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

                    # Nhận diện khuôn mặt
                    face_locations = face_recognition.face_locations(rgb_image)
                    if len(face_locations) > 0:
                        for (top, right, bottom, left) in face_locations:
                            face_image = rgb_image[top:bottom, left:right]
                            faces.append(face_image)
                            Ids.append(Id)  # ID phải là số nguyên

    return faces, Ids, len(unique_ids)
def getProfile(id):
    conn = sqlite3.connect("FaceBaseNew.db")
    cursor = conn.execute("SELECT * FROM People WHERE ID=" + str(id))
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile


def TrackImages(tolerance=0.4, frame_resize_scale=0.5, process_every_n_frames=5, motion_threshold=50, min_time_between_records=60):
    # Kết nối đến cơ sở dữ liệu SQLite
    conn = sqlite3.connect('FaceBaseNew.db')
    cursor = conn.cursor()

    # Đọc file encodings
    encodings_path = os.path.join(os.getcwd(), "encodings", "encodings.pickle")
    with open(encodings_path, "rb") as f:
        data = pickle.load(f)

    cam = cv2.VideoCapture(0)
    cam.set(3, 1920)
    cam.set(4, 1080)
    font = cv2.FONT_HERSHEY_SIMPLEX

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')

    frame_count = 0  # Đếm số khung hình đã xử lý
    prev_frame = None  # Khung hình trước

    # Dictionary để lưu thời gian ghi nhận lần cuối cùng của mỗi ID
    last_recorded_time = {}

    while True:
        ret, im = cam.read()
        frame_count += 1

        # Chỉ xử lý sau mỗi n khung hình
        if frame_count % process_every_n_frames != 0:
            continue

        # Giảm kích thước khung hình
        small_frame = cv2.resize(im, (0, 0), fx=frame_resize_scale, fy=frame_resize_scale)
        rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Chuyển đổi khung hình sang màu xám để so sánh
        gray_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is None:
            prev_frame = gray_frame
            continue

        # Tính độ khác biệt giữa khung hình hiện tại và khung hình trước
        frame_diff = cv2.absdiff(prev_frame, gray_frame)
        thresh = cv2.threshold(frame_diff, motion_threshold, 255, cv2.THRESH_BINARY)[1]
        motion_detected = cv2.countNonZero(thresh) > 5000  # Kiểm tra xem có chuyển động không

        if motion_detected:
            # Phát hiện khuôn mặt trong khung hình đã thay đổi kích thước
            boxes = face_recognition.face_locations(rgb, model="hog")
            encodings = face_recognition.face_encodings(rgb, boxes)

            for (box, encoding) in zip(boxes, encodings):
                matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=tolerance)
                name = "Unknown"

                face_distances = face_recognition.face_distance(data["encodings"], encoding)
                if True in matches:
                    best_match_index = face_distances.argmin()
                    if matches[best_match_index]:
                        name = data["names"][best_match_index]
                        name = remove_accent(name)  # Chuyển thành không dấu

                (top, right, bottom, left) = [int(pos / frame_resize_scale) for pos in box]
                cv2.rectangle(im, (left, top), (right, bottom), (225, 0, 0), 2)

                if name != "Unknown":
                    try:
                        Id = int(name.split('_')[-1])  # Chuyển đổi name về dạng int (Id)
                    except (IndexError, ValueError):
                        continue

                    profile = getProfile(Id)

                    if profile is not None:
                        current_time = time.time()

                        if Id in last_recorded_time:
                            time_since_last_record = current_time - last_recorded_time[Id]
                            if time_since_last_record < min_time_between_records:
                                continue  # Bỏ qua nếu chưa đủ thời gian

                        last_recorded_time[Id] = current_time

                        ts = time.time()
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        aa = profile[1]
                        name = remove_accent(aa)  # Chuyển thành không dấu
                        arrId = []
                        cursor.execute(
                            "SELECT PersonId FROM Attendance WHERE PersonId = ? AND Date = ? AND Status = 'In'",
                            (Id, date))
                        rows = cursor.fetchall()

                        for row in rows:
                            arrId.append(row[0])

                        if arrId.count(Id) == 0:
                            status = 'In'
                            show_message_and_wait("Xác nhận", f"Xác nhận ghi nhận {aa} checkin lúc {timeStamp}?")
                            cursor.execute("INSERT INTO Attendance (PersonId, Date, Time, Status) VALUES (?, ?, ?, ?)",
                                           (Id, date, timeStamp, status))
                            cursor.execute(
                                "INSERT INTO AttendanceStatistic (PersonId, Date, TimeIn, TimeOut, TotalTime) VALUES (?, ?, ?, ?, ?)",
                                (Id, date, timeStamp, '00:00:00', '0'))
                            conn.commit()

                        elif arrId.count(Id) == 1:
                            status = 'Out'
                            show_message_and_wait("Xác nhận", f"Xác nhận ghi nhận {aa} checkout lúc {timeStamp}?")
                            cursor.execute(
                                "SELECT TimeIn FROM AttendanceStatistic WHERE PersonId = ? AND Date = ?", (Id, date))
                            row = cursor.fetchone()

                            if row:
                                time_in_str = row[0]
                                total_time = (datetime.datetime.strptime(timeStamp, '%H:%M:%S') -
                                              datetime.datetime.strptime(time_in_str, '%H:%M:%S')).total_seconds()

                                cursor.execute(
                                    "INSERT INTO Attendance (PersonId, Date, Time, Status) VALUES (?, ?, ?, ?)",
                                    (Id, date, timeStamp, status))
                                cursor.execute(
                                    "UPDATE AttendanceStatistic SET TimeOut = ?, TotalTime = ? WHERE PersonId = ? AND Date = ?",
                                    (timeStamp, total_time, Id, date))
                                conn.commit()

                        cv2.putText(im, "Id: " + str(profile[0]), (left, bottom + 30), font, 0.75, (255, 255, 255), 2)
                        cv2.putText(im, "Name: " + name, (left, bottom + 60), font, 0.75, (255, 255, 255), 2)
                    else:
                        cv2.putText(im, "Name: Unknown", (left, bottom + 30), font, 0.75, (0, 0, 255), 2)
                else:
                    cv2.putText(im, "Name: Unknown", (left, bottom + 30), font, 0.75, (0, 0, 255), 2)

        prev_frame = gray_frame.copy()

        cv2.imshow('im', im)

        if cv2.waitKey(1) == ord('q'):
            break

    conn.close()
    cam.release()
    cv2.destroyAllWindows()




