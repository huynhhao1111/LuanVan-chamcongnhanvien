import tkinter as tk
from tkinter import filedialog
from tkinter import Message, Text
import cv2, os
import shutil
import csv

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


def insertOrUpdate(id, name, age, gender, cr):
    conn = sqlite3.connect("FaceBaseNew.db")
    cursor = conn.execute('SELECT * FROM People WHERE ID=' + str(id))
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
        break

    if isRecordExist == 1:
        cmd = "UPDATE people SET Name=' " + str(name) + " ',Age=' " + str(age) + " ',Gender=' " + str(
            gender) + " ',CR=' " + str(cr) + " ' WHERE ID=" + str(id)
    else:
        cmd = "INSERT INTO people(ID,Name,Age,Gender,CR) Values(" + str(id) + ",' " + str(name) + " ',' " + str(
            age) + " ',' " + str(gender) + " ',' " + str(cr) + " ' )"
    conn.execute(cmd)
    conn.commit()
    conn.close()


import cv2
import os
import shutil
import time
from tkinter import messagebox as msgbox

def TakeImages(Id, name, age, gender, cr):
    if is_number(Id) and name.isalpha():
        insertOrUpdate(Id, name, age, gender, cr)
        cam = cv2.VideoCapture(0)
        cam.set(3, 1920)
        cam.set(4, 1080)

        sampleNum = 0

        # Tạo thư mục theo tên của người dùng và ID
        folder_name = f"TrainingImage/{name}_{Id}"
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name)  # Xóa toàn bộ ảnh cũ
        os.makedirs(folder_name)  # Tạo lại thư mục mới

        while True:
            ret, frame = cam.read()
            if not ret:
                print("Không thể truy cập webcam!")
                break

            # Hiển thị số lượng ảnh đã lưu
            cv2.putText(frame, f'Sample: {sampleNum}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow('frame', frame)

            # Kiểm tra và lưu ảnh sau mỗi 0.2 giây
            if sampleNum < 70:  # Giới hạn số lượng mẫu
                # Lưu ảnh vào thư mục
                image_path = os.path.join(folder_name, f"{name}_{Id}_{sampleNum + 1}.jpg")
                cv2.imwrite(image_path, frame)
                print(f"Lưu ảnh: {image_path}")

                sampleNum += 1  # Tăng số mẫu đã chụp

                # Tạm dừng 0.2 giây
                time.sleep(0.2)

            # Điều kiện thoát nếu đã chụp đủ 70 ảnh
            if sampleNum >= 70:
                print("Đã chụp đủ 70 ảnh.")
                break

            # Điều kiện thoát khác
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()

        # Thông báo cho người dùng
        user_choice = msgbox.askquestion("Thông báo", "Bạn đã lấy đủ ảnh. Tiến hành lấy dữ liệu khuôn mặt? Chọn 'Yes' để lấy dữ liệu hoặc 'No' để lấy lại hình ảnh.")

        if user_choice == 'yes':
            # Gọi hàm TrainImages để thêm dữ liệu cho người vừa lấy
            TrainImages(folder_name, f"{name}_{Id}")
            msgbox.showinfo("Thông báo", f"Dữ liệu khuôn mặt của bạn đã được mã hóa và lưu vào file encodings.pickle với ID: {Id}, Name: {name}")
        else:
            # Nếu người dùng chọn lấy lại hình ảnh, mở lại webcam
            print("Mở lại webcam để lấy lại hình ảnh...")
            TakeImages(Id, name, age, gender, cr)  # Gọi lại hàm để lấy lại hình ảnh
    else:
        if not is_number(Id):
            res = "Nhập ID là số"
            msgbox.showerror('Error', res)
        if not name.isalpha():
            res = "Nhập tên theo thứ tự bảng chữ cái"
            msgbox.showerror('Error', res)

def TrainImages(training_dir, person_name):
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
        return

    # Tạo thư mục lưu encodings nếu chưa tồn tại
    if not os.path.exists("encodings"):
        os.makedirs("encodings")

    # Lưu dữ liệu mã hóa mới vào tệp encodings.pickle
    data = {"encodings": encodings, "names": names}
    with open("encodings/encodings.pickle", "wb") as f:
        f.write(pickle.dumps(data))

    print("[INFO] Đã hoàn thành huấn luyện và lưu mã hóa.")

# def TakeImages(Id, name, age, gender, cr):
#     if (is_number(Id) and name.isalpha()):
#         insertOrUpdate(Id, name, age, gender, cr)
#         cam = cv2.VideoCapture(0)
#         cam.set(3, 1920)
#         cam.set(4, 1080)
#
#         sampleNum = 0
#
#         # Tạo thư mục theo tên của người dùng và ID
#         folder_name = f"TrainingImage/{name}_{Id}"
#         if os.path.exists(folder_name):
#             shutil.rmtree(folder_name)  # Xóa toàn bộ ảnh cũ
#         os.makedirs(folder_name)  # Tạo lại thư mục mới
#
#         while True:
#             ret, frame = cam.read()
#             if not ret:
#                 print("Không thể truy cập webcam!")
#                 break
#
#             sampleNum += 1
#
#             # Lưu ảnh vào thư mục
#             image_path = os.path.join(folder_name, f"{name}_{Id}_{sampleNum}.jpg")
#             cv2.imwrite(image_path, frame)
#
#             # Hiển thị số lượng ảnh đã lưu
#             cv2.putText(frame, f'Sample: {sampleNum}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
#                         (255, 0, 0), 2)
#             cv2.imshow('frame', frame)
#
#             # Điều kiện thoát
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#             if sampleNum >= 100:  # Giới hạn số lượng mẫu
#                 print("Đã chụp đủ 100 ảnh.")
#                 break
#
#         cam.release()
#         cv2.destroyAllWindows()
#
#         # Thông báo cho người dùng
#         user_choice = msgbox.askquestion("Thông báo", "Bạn đã lấy đủ ảnh. Tiến hành lấy dữ liệu khuôn mặt? Chọn 'Lấy dữ liệu' hoặc 'Lấy lại hình ảnh'.")
#
#         if user_choice == 'yes':
#             # Gọi hàm TrainImage chỉ để thêm dữ liệu cho người vừa lấy
#             TrainImages(folder_name)
#             msgbox.showinfo("Thông báo", f"Dữ liệu khuôn mặt của bạn đã được mã hóa và lưu vào file encodings.pickle với ID: {Id}, Name: {name}")
#         else:
#             # Nếu người dùng chọn lấy lại hình ảnh, mở lại webcam
#             print("Mở lại webcam để lấy lại hình ảnh...")
#             TakeImages(Id, name, age, gender, cr)  # Gọi lại hàm để lấy lại hình ảnh
#     else:
#         if not is_number(Id):
#             res = "Nhập ID là số"
#             msgbox.showerror('Error', res)
#         if not name.isalpha():
#             res = "Nhập tên theo thứ tự bảng chữ cái"
#             msgbox.showerror('Error', res)
#
# def TrainImages(training_dir):
#     print("[INFO] bắt đầu huấn luyện...")
#
#     encodings = []
#     names = []
#
#     # Duyệt qua tất cả các thư mục con trong thư mục training_dir
#     for person_name in os.listdir(training_dir):
#         person_path = os.path.join(training_dir, person_name)
#
#         # Kiểm tra xem đó có phải là thư mục không
#         if os.path.isdir(person_path):
#             # Duyệt qua từng file ảnh trong thư mục của nhân viên
#             for image_name in os.listdir(person_path):
#                 image_path = os.path.join(person_path, image_name)
#
#                 # Đọc ảnh
#                 image = cv2.imread(image_path)
#                 rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#
#                 # Nhận diện khuôn mặt và mã hóa
#                 boxes = face_recognition.face_locations(rgb_image, model="hog")
#                 encodings_face = face_recognition.face_encodings(rgb_image, boxes)
#
#                 # Lưu mã hóa và tên vào danh sách
#                 for encoding in encodings_face:
#                     encodings.append(encoding)
#                     names.append(person_name)
#
#     # Lưu dữ liệu mã hóa vào file encodings.pickle
#     if not os.path.exists("encodings"):
#         os.makedirs("encodings")
#     data = {"encodings": encodings, "names": names}
#     with open("encodings/encodings.pickle", "wb") as f:
#         f.write(pickle.dumps(data))
#
#     print("[INFO] đã hoàn thành huấn luyện và lưu mã hóa.")
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

# def TakeImages(Id, name, age, gender, cr):
#     if (is_number(Id) and name.isalpha()):
#         insertOrUpdate(Id, name, age, gender, cr)
#         cam = cv2.VideoCapture(0)
#         cam.set(3, 1920)
#         cam.set(4, 1080)
#         # # load model haarcascade
#         # harcascadePath = "haarcascade_frontalface_default.xml"
#         # detector = cv2.CascadeClassifier(harcascadePath)
#
#         sampleNum = 0
#
#         # Tạo thư mục theo tên của người dùng và ID
#         folder_name = f"TrainingImage/{name}_{Id}"
#         if os.path.exists(folder_name):
#             shutil.rmtree(folder_name)  # Xóa toàn bộ ảnh cũ
#         os.makedirs(folder_name)  # Tạo lại thư mục mới
#
#         while True:
#             # ret, img = cam.read()
#             # # chuyển về ảnh xám
#             # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             # # nhận diện khuôn mặt
#             # faces = detector.detectMultiScale(gray, 1.3, 5)
#             # for (x, y, w, h) in faces:
#             #     # vẽ 1 đường bao quanh khuôn mặt
#             #     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
#             #     # số mẫu tăng dần
#             #     sampleNum += 1
#             #     # lưu khuôn mặt đã chụp vào thư mục theo tên
#             #     cv2.imwrite(f"{folder_name}/{name}_{Id}_{sampleNum}.jpg", gray[y:y + h, x:x + w])
#             #     cv2.putText(img, str(sampleNum), (x, y + h + 30), fontface, fontscale, fontcolor, 2)
#             #     # hiển thị khung
#             #     cv2.imshow('frame', img)
#             #
#             # # đợi trong 100 mili giây
#             # if cv2.waitKey(100) & 0xFF == ord('q'):
#             #     break
#             # # phá vỡ nếu số lượng mẫu nhiều hơn 100
#             # elif sampleNum > 100:
#             #     break
#             # Đọc ảnh từ webcam
#             ret, frame = cam.read()
#             if not ret:
#                 print("Không thể truy cập webcam!")
#                 break
#
#             # Chuyển đổi ảnh từ BGR sang RGB cho face_recognition
#             # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#             # Tìm khuôn mặt trong ảnh
#             # face_locations = face_recognition.face_locations(rgb_frame)
#
#             # Nếu phát hiện ít nhất một khuôn mặt
#             # if len(face_locations) > 0:
#                 # # Cắt khuôn mặt đầu tiên được phát hiện
#                 # top, right, bottom, left = face_locations[0]
#                 # face_image = frame[top:bottom, left:right]
#                 #
#                 # # Lưu ảnh khuôn mặt vào thư mục
#                 # image_path = os.path.join(folder_name, f"{name}_{Id}_{sampleNum}.jpg")
#                 # cv2.imwrite(image_path, face_image)
#                 # sampleNum += 1
#                 #
#                 # # Hiển thị số lượng ảnh đã lưu
#                 # print(f"Đã lưu ảnh {sampleNum}: {image_path}")
#                 # for (top, right, bottom, left) in face_locations:
#                 #     cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
#             sampleNum += 1
#
#                     # Lưu ảnh khuôn mặt vào thư mục
#                     # gray_face = cv2.cvtColor(frame[top:bottom, left:right], cv2.COLOR_BGR2GRAY)
#
#             image_path = os.path.join(folder_name, f"{name}_{Id}_{sampleNum}.jpg")
#             cv2.imwrite(image_path, frame)
#
#                     # Hiển thị số lượng ảnh đã lưu
#             cv2.putText(frame, f'Sample: {sampleNum}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
#                             (255, 0, 0), 2)
#             # Hiển thị khung hình
#             cv2.imshow('frame', frame)
#             # Điều kiện thoát
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                     break
#             # Điều kiện thoát
#             if sampleNum >= 100:  # Giới hạn số lượng mẫu
#                 print("Đã chụp đủ 100 ảnh.")
#                 break
#
#         cam.release()
#         cv2.destroyAllWindows()
#
#         msgbox.showinfo("Thông báo", f"Ảnh của bạn đã được lưu với ID: {Id}, Name: {name}")
#     else:
#         if not is_number(Id):
#             res = "Nhập ID là số"
#             msgbox.showerror('Error', res)
#         if not name.isalpha():
#             res = "Nhập tên theo thứ tự bảng chữ cái"
#             msgbox.showerror('Error', res)
def extract_images_from_video(Id, name, age, gender, cr):
    if is_number(Id) and name.isalpha():
        insertOrUpdate(Id, name, age, gender, cr)
        # Chọn video để lấy ảnh
        video_path = filedialog.askopenfilename(title="Chọn video", filetypes=[("Video Files", "*.mp4 *.avi *.mov")])

        if not video_path:
            return  # Nếu không chọn video nào thì thoát khỏi hàm

        # Tạo thư mục theo tên của người dùng và ID
        folder_name = f"TrainingImage/{name}_{Id}"
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name)  # Xóa toàn bộ ảnh cũ nếu có
        os.makedirs(folder_name)  # Tạo lại thư mục mới

        # Khởi tạo đối tượng video
        cap = cv2.VideoCapture(video_path)
        sampleNum = 0

        # Thời gian chụp ảnh
        last_capture_time = time.time()  # Lưu thời gian lần chụp cuối

        while cap.isOpened():
            # Đọc từng khung hình từ video
            ret, frame = cap.read()
            if not ret:
                print("Không thể đọc khung hình từ video!")
                break

            # Kiểm tra thời gian chụp ảnh
            current_time = time.time()
            if current_time - last_capture_time >= 0.1:  # Nếu đã qua 1 giây
                # Tăng số mẫu ảnh đã lấy
                sampleNum += 1

                # Lưu ảnh vào thư mục
                image_path = os.path.join(folder_name, f"{name}_{Id}_{sampleNum}.jpg")
                cv2.imwrite(image_path, frame)

                # Cập nhật thời gian chụp ảnh
                last_capture_time = current_time

                # Hiển thị số lượng ảnh đã lưu
                cv2.putText(frame, f'Sample: {sampleNum}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.imshow('Video', frame)

            # Điều kiện thoát: nhấn phím 'q' để dừng
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Giới hạn số lượng ảnh là 70
            if sampleNum >= 70:
                print("Đã chụp đủ 70 ảnh.")
                break

        # Giải phóng tài nguyên
        cap.release()
        cv2.destroyAllWindows()

        # Thông báo cho người dùng
        user_choice = msgbox.askquestion("Thông báo", "Bạn đã lấy đủ ảnh. Tiến hành lấy dữ liệu khuôn mặt? Chọn 'Yes' để lấy dữ liệu hoặc 'No' để lấy lại hình ảnh.")

        if user_choice == 'yes':
            # Gọi hàm TrainImages để thêm dữ liệu cho người vừa lấy
            TrainImages(folder_name, f"{name}_{Id}")
            msgbox.showinfo("Thông báo", f"Dữ liệu khuôn mặt của bạn đã được mã hóa ID: {Id}, Tên Nhân Viên: {name}")
        else:
            # Nếu người dùng chọn lấy lại hình ảnh, mở lại video
            print("Mở lại video để lấy lại hình ảnh...")
            extract_images_from_video(Id, name, age, gender, cr)  # Gọi lại hàm để lấy lại hình ảnh
    else:
        if not is_number(Id):
            msgbox.showerror('Error', "Nhập ID là số")
        if not name.isalpha():
            msgbox.showerror('Error', "Nhập tên theo thứ tự bảng chữ cái")


# def extract_images_from_video(Id, name, age, gender, cr):
#     if is_number(Id) and name.isalpha():
#         insertOrUpdate(Id, name, age, gender, cr)
#         video_path = filedialog.askopenfilename(title="Chọn video", filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
#
#         if not video_path:
#             return
#
#         # Tạo thư mục theo tên của người dùng và ID
#         folder_name = f"TrainingImage/{name}_{Id}"
#         if os.path.exists(folder_name):
#             shutil.rmtree(folder_name)  # Xóa toàn bộ ảnh cũ nếu có
#         os.makedirs(folder_name)  # Tạo lại thư mục mới
#
#         # Khởi tạo video
#         cap = cv2.VideoCapture(video_path)
#         sampleNum = 0
#
#         while cap.isOpened():
#             # Đọc từng khung hình từ video
#             ret, frame = cap.read()
#             if not ret:
#                 print("Không thể đọc khung hình từ video!")
#                 break
#
#             # Số mẫu tăng dần
#             sampleNum += 1
#
#             # Lưu ảnh vào thư mục
#             image_path = os.path.join(folder_name, f"{name}_{Id}_{sampleNum}.jpg")
#             cv2.imwrite(image_path, frame)
#
#             # Hiển thị số lượng ảnh đã lưu
#             cv2.putText(frame, f'Sample: {sampleNum}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
#             cv2.imshow('Video', frame)
#
#             # Điều kiện thoát
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#             # Giới hạn số lượng ảnh là 100
#             if sampleNum >= 100:
#                 print("Đã chụp đủ 100 ảnh.")
#                 break
#
#         # Giải phóng tài nguyên
#         cap.release()
#         cv2.destroyAllWindows()
#
#         msgbox.showinfo("Thông báo", f"Ảnh của bạn đã được lưu với ID: {Id}, Name: {name}")
#     else:
#         if not is_number(Id):
#             msgbox.showerror('Error', "Nhập ID là số")
#         if not name.isalpha():
#             msgbox.showerror('Error', "Nhập tên theo thứ tự bảng chữ cái")



import cv2
import os
import pickle
import face_recognition


# def TrainImages(training_dir):
#     print("[INFO] bắt đầu huấn luyện...")
#
#     encodings = []
#     names = []
#
#     # Duyệt qua tất cả các thư mục con trong thư mục training_dir
#     for person_name in os.listdir(training_dir):
#         person_path = os.path.join(training_dir, person_name)
#
#         # Kiểm tra xem đó có phải là thư mục không
#         if os.path.isdir(person_path):
#             # Duyệt qua từng file ảnh trong thư mục của nhân viên
#             for image_name in os.listdir(person_path):
#                 image_path = os.path.join(person_path, image_name)
#
#                 # Đọc ảnh
#                 image = cv2.imread(image_path)
#                 rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#
#                 # Nhận diện khuôn mặt và mã hóa
#                 boxes = face_recognition.face_locations(rgb_image, model="hog")
#                 encodings_face = face_recognition.face_encodings(rgb_image, boxes)
#
#                 # Lưu mã hóa và tên vào danh sách
#                 for encoding in encodings_face:
#                     encodings.append(encoding)
#                     names.append(person_name)
#
#     # Lưu dữ liệu mã hóa vào file encodings.pickle
#     data = {"encodings": encodings, "names": names}
#     with open("encodings/encodings.pickle", "wb") as f:
#         f.write(pickle.dumps(data))
#
#     print("[INFO] đã hoàn thành huấn luyện và lưu mã hóa.")



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

import numpy as np  # Thêm thư viện numpy

def TrackImages(tolerance=0.4, frame_resize_scale=0.5, process_every_n_frames=3, motion_threshold=50):
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
    fileName = r"Attendance\Attendance_" + date + ".csv"
    fileName_statistic = r"AttendanceStatistic\AttendanceStatistic_" + date + ".csv"
    col_names = ['Id', 'Name', 'Date', 'Time', 'Status']
    col_name_statistic = ['Id', 'Name', 'Date', 'Time In', 'Time Out', 'Total time']
    attendance = pd.DataFrame(columns=col_names)
    attendance_statistic = pd.DataFrame(columns=col_name_statistic)

    frame_count = 0  # Đếm số khung hình đã xử lý
    prev_frame = None  # Khung hình trước
    message = ""  # Khởi tạo biến thông báo
    message_time = 0  # Thời gian hiển thị thông báo

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
        motion_detected = cv2.countNonZero(thresh) > 1000  # Kiểm tra xem có chuyển động không

        if motion_detected:
            # Phát hiện khuôn mặt trong khung hình đã thay đổi kích thước
            boxes = face_recognition.face_locations(rgb, model="hog")
            encodings = face_recognition.face_encodings(rgb, boxes)

            for (box, encoding) in zip(boxes, encodings):
                # So sánh với encodings đã biết
                matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=tolerance)
                name = "Unknown"

                # Kiểm tra nếu có khớp giữa các encodings
                face_distances = face_recognition.face_distance(data["encodings"], encoding)
                best_match_index = None
                if True in matches:
                    # Lấy chỉ số của khuôn mặt khớp nhất
                    best_match_index = face_distances.argmin()
                    if matches[best_match_index]:
                        name = data["names"][best_match_index]

                # Tính toán lại vị trí của khung mặt trên khung hình gốc
                (top, right, bottom, left) = [int(pos / frame_resize_scale) for pos in box]
                cv2.rectangle(im, (left, top), (right, bottom), (225, 0, 0), 2)

                if name != "Unknown":
                    # Tách phần số từ tên ID nếu cần thiết
                    try:
                        Id = int(name.split('_')[1])  # Chuyển đổi name về dạng int (Id)
                    except (IndexError, ValueError):
                        print(f"Invalid ID format: {name}")
                        continue  # Bỏ qua nếu không thể chuyển đổi

                    profile = getProfile(Id)

                    if profile is not None:
                        # Cập nhật file attendance
                        arrId = []
                        if os.path.isfile(fileName):
                            with open(fileName) as f:
                                reader = csv.reader(f)
                                for row in reader:
                                    if row[0] == str(Id):
                                        arrId.append(Id)

                        if arrId.count(Id) == 0:
                            ts = time.time()
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            aa = profile[1]
                            status = 'In'
                            attendance.loc[len(attendance)] = [Id, aa, date, timeStamp, status]
                            attendance_statistic.loc[len(attendance_statistic)] = [Id, aa, date, timeStamp, '0', '0']
                            message = f"Diem Danh {aa} Vao Ca Thanh Cong"  # Cập nhật thông báo
                            message_time = time.time()  # Lưu thời gian hiển thị thông báo

                        elif arrId.count(Id) == 1:
                            ts = time.time()
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            aa = profile[1]
                            status = 'Out'
                            attendance.loc[len(attendance)] = [Id, aa, date, timeStamp, status]
                            message = f"Diem Danh {aa} Ra Ca Thanh Cong"  # Cập nhật thông báo
                            message_time = time.time()  # Lưu thời gian hiển thị thông báo
                            df = pd.read_csv(fileName_statistic)

                            with open(fileName_statistic) as f:
                                reader = csv.reader(f)
                                index = df.index[df['Id'] == Id].tolist()
                                for row in reader:
                                    if row[0] == str(Id):
                                        df.loc[index[0], 'Time Out'] = timeStamp
                                        df.loc[index[0], 'Total time'] = (
                                            datetime.datetime.strptime(timeStamp, '%H:%M:%S') -
                                            datetime.datetime.strptime(row[3], '%H:%M:%S')).total_seconds()
                                        df.to_csv(fileName_statistic, index=False)

                        cv2.putText(im, "Id: " + str(profile[0]), (left, bottom + 30), font, 0.75, (255, 255, 255), 2)
                        cv2.putText(im, "Name: " + str(profile[1]), (left, bottom + 60), font, 0.75, (255, 255, 255), 2)
                    else:
                        cv2.putText(im, "Name: Unknown", (left, bottom + 30), font, 0.75, (0, 0, 255), 2)
                else:
                    cv2.putText(im, "Name: Unknown", (left, bottom + 30), font, 0.75, (0, 0, 255), 2)

            attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
            attendance_statistic = attendance_statistic.drop_duplicates(subset=['Id'], keep='first')

        # Cập nhật khung hình trước
        prev_frame = gray_frame.copy()

        # Hiển thị thông báo nếu có
        if message and (time.time() - message_time <= 3):  # Hiển thị trong 3 giây
            # Tạo nền màu xanh cho thông báo
            cv2.rectangle(im, (0, im.shape[0] - 60), (im.shape[1], im.shape[0]), (0, 255, 0), -1)  # Nền xanh
            cv2.putText(im, message, (10, im.shape[0] - 30), font, 0.75, (255, 255, 255), 2)  # Văn bản trắng

        cv2.imshow('im', im)

        if cv2.waitKey(1) == ord('q'):
            break

    if os.path.isfile(fileName):
        attendance.to_csv(fileName, mode='a', index=False, header=False)
    else:
        attendance.to_csv(fileName, mode='a', index=False)

    if os.path.isfile(fileName_statistic):
        attendance_statistic.to_csv(fileName_statistic, mode='a', index=False, header=False)
    else:
        attendance_statistic.to_csv(fileName_statistic, mode='a', index=False)

    cam.release()
    cv2.destroyAllWindows()

# def TrackImages(tolerance=0.4, frame_resize_scale=0.5, process_every_n_frames=3, motion_threshold=50):
#     # Đọc file encodings
#     encodings_path = os.path.join(os.getcwd(), "encodings", "encodings.pickle")
#     with open(encodings_path, "rb") as f:
#         data = pickle.load(f)
#
#     cam = cv2.VideoCapture(0)
#     cam.set(3, 1920)
#     cam.set(4, 1080)
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     ts = time.time()
#     date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
#     fileName = r"Attendance\Attendance_" + date + ".csv"
#     fileName_statistic = r"AttendanceStatistic\AttendanceStatistic_" + date + ".csv"
#     col_names = ['Id', 'Name', 'Date', 'Time', 'Status']
#     col_name_statistic = ['Id', 'Name', 'Date', 'Time In', 'Time Out', 'Total time']
#     attendance = pd.DataFrame(columns=col_names)
#     attendance_statistic = pd.DataFrame(columns=col_name_statistic)
#
#     frame_count = 0  # Đếm số khung hình đã xử lý
#     prev_frame = None  # Khung hình trước
#
#     while True:
#         ret, im = cam.read()
#         frame_count += 1
#
#         # Chỉ xử lý sau mỗi n khung hình
#         if frame_count % process_every_n_frames != 0:
#             continue
#
#         # Giảm kích thước khung hình
#         small_frame = cv2.resize(im, (0, 0), fx=frame_resize_scale, fy=frame_resize_scale)
#         rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
#
#         # Chuyển đổi khung hình sang màu xám để so sánh
#         gray_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
#
#         if prev_frame is None:
#             prev_frame = gray_frame
#             continue
#
#         # Tính độ khác biệt giữa khung hình hiện tại và khung hình trước
#         frame_diff = cv2.absdiff(prev_frame, gray_frame)
#         thresh = cv2.threshold(frame_diff, motion_threshold, 255, cv2.THRESH_BINARY)[1]
#         motion_detected = cv2.countNonZero(thresh) > 1000  # Kiểm tra xem có chuyển động không
#
#         if motion_detected:
#             # Phát hiện khuôn mặt trong khung hình đã thay đổi kích thước
#             boxes = face_recognition.face_locations(rgb, model="hog")
#             encodings = face_recognition.face_encodings(rgb, boxes)
#
#             for (box, encoding) in zip(boxes, encodings):
#                 # So sánh với encodings đã biết
#                 matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=tolerance)
#                 name = "Unknown"
#
#                 # Kiểm tra nếu có khớp giữa các encodings
#                 face_distances = face_recognition.face_distance(data["encodings"], encoding)
#                 best_match_index = None
#                 if True in matches:
#                     # Lấy chỉ số của khuôn mặt khớp nhất
#                     best_match_index = face_distances.argmin()
#                     if matches[best_match_index]:
#                         name = data["names"][best_match_index]
#
#                 # Tính toán lại vị trí của khung mặt trên khung hình gốc
#                 (top, right, bottom, left) = [int(pos / frame_resize_scale) for pos in box]
#                 cv2.rectangle(im, (left, top), (right, bottom), (225, 0, 0), 2)
#
#                 if name != "Unknown":
#                     # Tách phần số từ tên ID nếu cần thiết
#                     try:
#                         Id = int(name.split('_')[1])  # Chuyển đổi name về dạng int (Id)
#                     except (IndexError, ValueError):
#                         print(f"Invalid ID format: {name}")
#                         continue  # Bỏ qua nếu không thể chuyển đổi
#
#                     profile = getProfile(Id)
#
#                     if profile is not None:
#                         # Cập nhật file attendance
#                         arrId = []
#                         if os.path.isfile(fileName):
#                             with open(fileName) as f:
#                                 reader = csv.reader(f)
#                                 for row in reader:
#                                     if row[0] == str(Id):
#                                         arrId.append(Id)
#
#                         if arrId.count(Id) == 0:
#                             ts = time.time()
#                             timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
#                             aa = profile[1]
#                             status = 'In'
#                             attendance.loc[len(attendance)] = [Id, aa, date, timeStamp, status]
#                             attendance_statistic.loc[len(attendance_statistic)] = [Id, aa, date, timeStamp, '0', '0']
#
#                         elif arrId.count(Id) == 1:
#                             ts = time.time()
#                             timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
#                             aa = profile[1]
#                             status = 'Out'
#                             attendance.loc[len(attendance)] = [Id, aa, date, timeStamp, status]
#                             df = pd.read_csv(fileName_statistic)
#
#                             with open(fileName_statistic) as f:
#                                 reader = csv.reader(f)
#                                 index = df.index[df['Id'] == Id].tolist()
#                                 for row in reader:
#                                     if row[0] == str(Id):
#                                         df.loc[index[0], 'Time Out'] = timeStamp
#                                         df.loc[index[0], 'Total time'] = (
#                                             datetime.datetime.strptime(timeStamp, '%H:%M:%S') -
#                                             datetime.datetime.strptime(row[3], '%H:%M:%S')).total_seconds()
#                                         df.to_csv(fileName_statistic, index=False)
#
#                         cv2.putText(im, "Id: " + str(profile[0]), (left, bottom + 30), font, 0.75, (255, 255, 255), 2)
#                         cv2.putText(im, "Name: " + str(profile[1]), (left, bottom + 60), font, 0.75, (255, 255, 255), 2)
#                     else:
#                         cv2.putText(im, "Name: Unknown", (left, bottom + 30), font, 0.75, (0, 0, 255), 2)
#                 else:
#                     cv2.putText(im, "Name: Unknown", (left, bottom + 30), font, 0.75, (0, 0, 255), 2)
#
#             attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
#             attendance_statistic = attendance_statistic.drop_duplicates(subset=['Id'], keep='first')
#
#         # Cập nhật khung hình trước
#         prev_frame = gray_frame.copy()
#         cv2.imshow('im', im)
#
#         if cv2.waitKey(1) == ord('q'):
#             break
#
#     if os.path.isfile(fileName):
#         attendance.to_csv(fileName, mode='a', index=False, header=False)
#     else:
#         attendance.to_csv(fileName, mode='a', index=False)
#
#     if os.path.isfile(fileName_statistic):
#         attendance_statistic.to_csv(fileName_statistic, mode='a', index=False, header=False)
#     else:
#         attendance_statistic.to_csv(fileName_statistic, mode='a', index=False)
#
#     cam.release()
#     cv2.destroyAllWindows()
#     msgbox.showinfo("Message", 'Bạn đã chấm công thành công!')


