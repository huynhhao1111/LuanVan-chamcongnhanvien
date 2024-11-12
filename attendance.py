import sqlite3
import tkinter as tk
from tkinter import ttk
import datetime


# Hàm tìm kiếm điểm danh theo ID
def search_attendance(tree, id_entry):
    search_id = id_entry.get()  # Lấy ID từ ô nhập liệu
    today = datetime.datetime.now().strftime('%d-%m-%Y')  # Lấy ngày theo định dạng dd-mm-yy
    print("Ngày hôm nay:", today)  # In ra ngày hôm nay để kiểm tra

    # Xóa tất cả các mục hiện tại trong bảng
    for item in tree.get_children():
        tree.delete(item)

    try:
        # Kết nối đến cơ sở dữ liệu SQLite
        conn = sqlite3.connect('FaceBaseNew.db')
        cursor = conn.cursor()

        # Nếu ô ID trống, tìm tất cả dữ liệu của ngày hôm nay
        if search_id == "":
            cursor.execute(''' 
                SELECT a.PersonId, p.Name, a.Date, a.Time, a.Status 
                FROM Attendance a
                JOIN People p ON a.PersonId = p.id
                WHERE a.Date = ?
            ''', (today,))
        else:
            # Truy vấn dữ liệu theo ngày hôm nay và ID người dùng
            cursor.execute(''' 
                SELECT a.PersonId, p.Name, a.Date, a.Time, a.Status 
                FROM Attendance a
                JOIN People p ON a.PersonId = p.id
                WHERE a.Date = ? AND a.PersonId = ?
            ''', (today, search_id))

        # Thêm các kết quả vào bảng Treeview
        rows = cursor.fetchall()
        for row in rows:
            person_id, name, date, time, status = row
            tree.insert("", "end", values=(person_id, name, date, time, status))

        # Đóng kết nối
        conn.close()
    except sqlite3.Error as e:
        print("Lỗi truy vấn cơ sở dữ liệu:", e)


# Hàm tạo giao diện
def attendance():
    root = tk.Tk()
    ts = datetime.datetime.now()
    date = ts.strftime('%d-%m-%Y')
    root.title("Kiểm tra chấm công ngày " + date)

    # Thiết lập kích thước cửa sổ
    width = 600
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(0, 0)

    # Khung chứa tiêu đề
    header_frame = tk.Frame(root, bg='#4CAF50')
    header_frame.pack(fill=tk.X)

    header_label = tk.Label(header_frame, text="Kiểm Tra Chấm Công", font=("Arial", 20, 'bold'), bg='#4CAF50',
                            fg='white')
    header_label.pack(pady=10)

    # Khung tìm kiếm
    search_frame = tk.Frame(root)
    search_frame.pack(pady=10)

    id_label = tk.Label(search_frame, text="Nhập ID:", font=("Arial", 12))
    id_label.pack(side=tk.LEFT)

    id_entry = tk.Entry(search_frame, font=("Arial", 12))
    id_entry.pack(side=tk.LEFT, padx=5)

    search_button = tk.Button(search_frame, text="Tìm Kiếm", font=("Arial", 12),
                              command=lambda: search_attendance(tree, id_entry))
    search_button.pack(side=tk.LEFT)

    # Khung chứa bảng
    TableMargin = tk.Frame(root)
    TableMargin.pack(pady=20)

    # Thanh cuộn
    scrollbarx = tk.Scrollbar(TableMargin, orient=tk.HORIZONTAL)
    scrollbary = tk.Scrollbar(TableMargin, orient=tk.VERTICAL)

    # Bảng
    tree = ttk.Treeview(TableMargin, columns=("Id", "Name", "Date", "Time", "Status"), height=15,
                        selectmode="extended",
                        yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

    # Cấu hình thanh cuộn
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)

    # Tiêu đề bảng
    tree.heading('Id', text="Id", anchor=tk.W)
    tree.heading('Name', text="Name", anchor=tk.W)
    tree.heading('Date', text="Date", anchor=tk.W)
    tree.heading('Time', text="Time", anchor=tk.W)
    tree.heading('Status', text="Status", anchor=tk.W)

    # Cấu hình cột
    tree.column('#0', stretch=tk.NO, minwidth=0, width=0)
    tree.column('#1', stretch=tk.NO, minwidth=0, width=50)
    tree.column('#2', stretch=tk.NO, minwidth=0, width=150)
    tree.column('#3', stretch=tk.NO, minwidth=0, width=100)
    tree.column('#4', stretch=tk.NO, minwidth=0, width=100)

    # Thêm bảng vào khung
    tree.pack()
    # Gọi hàm search_attendance để hiển thị tất cả dữ liệu ngày hôm nay
    search_attendance(tree, id_entry)
    # Khởi động giao diện
    root.mainloop()

# if __name__ == "__main__":
#     attendance()

# from tkinter import *
# import tkinter.ttk as ttk
# import csv
# import datetime
# import time
#
#
# def search_attendance(tree, id_entry):
#     search_id = id_entry.get()
#     # Xóa tất cả các mục hiện tại trong bảng
#     for item in tree.get_children():
#         tree.delete(item)
#
#     # Đọc dữ liệu từ file CSV
#     date = datetime.datetime.now().strftime('%d-%m-%Y')
#     fileName = f"Attendance/Attendance_{date}.csv"
#     try:
#         with open(fileName) as f:
#             reader = csv.DictReader(f, delimiter=',')
#             for row in reader:
#                 if row['Id'] == search_id:  # Kiểm tra nếu ID khớp
#                     Id = row['Id']
#                     Name = row['Name']
#                     Date = row['Date']
#                     Time = row['Time']
#                     Status = row['Status']
#                     tree.insert("", "end", values=(Id, Name, Date, Time, Status))
#     except FileNotFoundError:
#         print("File không tìm thấy.")
#
#
# def attendance():
#     root = Tk()
#     ts = time.time()
#     date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
#     root.title("Kiểm tra chấm công ngày " + date)
#
#     # Thiết lập kích thước cửa sổ
#     width = 600
#     height = 500
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     x = (screen_width // 2) - (width // 2)
#     y = (screen_height // 2) - (height // 2)
#     root.geometry(f"{width}x{height}+{x}+{y}")
#     root.resizable(0, 0)
#
#     # Khung chứa tiêu đề
#     header_frame = Frame(root, bg='#4CAF50')
#     header_frame.pack(fill=X)
#
#     header_label = Label(header_frame, text="Kiểm Tra Chấm Công", font=("Arial", 20, 'bold'), bg='#4CAF50', fg='white')
#     header_label.pack(pady=10)
#
#     # Khung tìm kiếm
#     search_frame = Frame(root)
#     search_frame.pack(pady=10)
#
#     id_label = Label(search_frame, text="Nhập ID:", font=("Arial", 12))
#     id_label.pack(side=LEFT)
#
#     id_entry = Entry(search_frame, font=("Arial", 12))
#     id_entry.pack(side=LEFT, padx=5)
#
#     search_button = Button(search_frame, text="Tìm Kiếm", font=("Arial", 12),
#                            command=lambda: search_attendance(tree, id_entry))
#     search_button.pack(side=LEFT)
#
#     # Khung chứa bảng
#     TableMargin = Frame(root)
#     TableMargin.pack(pady=20)
#
#     # Thanh cuộn
#     scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
#     scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
#
#     # Bảng
#     tree = ttk.Treeview(TableMargin, columns=("Id", "Name", "Date", "Time", "Status"), height=15, selectmode="extended",
#                         yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
#
#     # Cấu hình thanh cuộn
#     scrollbary.config(command=tree.yview)
#     scrollbary.pack(side=RIGHT, fill=Y)
#     scrollbarx.config(command=tree.xview)
#     scrollbarx.pack(side=BOTTOM, fill=X)
#
#     # Tiêu đề bảng
#     tree.heading('Id', text="Id", anchor=W)
#     tree.heading('Name', text="Name", anchor=W)
#     tree.heading('Date', text="Date", anchor=W)
#     tree.heading('Time', text="Time", anchor=W)
#     tree.heading('Status', text="Status", anchor=W)
#
#     # Cấu hình cột
#     tree.column('#0', stretch=NO, minwidth=0, width=0)
#     tree.column('#1', stretch=NO, minwidth=0, width=50)
#     tree.column('#2', stretch=NO, minwidth=0, width=150)
#     tree.column('#3', stretch=NO, minwidth=0, width=100)
#     tree.column('#4', stretch=NO, minwidth=0, width=100)
#
#     # Thêm bảng vào khung
#     tree.pack()
#
#     # Đọc dữ liệu từ file CSV
#     fileName = f"Attendance/Attendance_{date}.csv"
#     try:
#         with open(fileName) as f:
#             reader = csv.DictReader(f, delimiter=',')
#             for row in reader:
#                 Id = row['Id']
#                 Name = row['Name']
#                 Date = row['Date']
#                 Time = row['Time']
#                 Status = row['Status']
#                 tree.insert("", "end", values=(Id, Name, Date, Time, Status))
#     except FileNotFoundError:
#         print("File không tìm thấy.")
#
#     # Khởi động giao diện
#     root.mainloop()
#
#
#
