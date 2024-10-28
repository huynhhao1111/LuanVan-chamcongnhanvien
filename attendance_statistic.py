from tkinter import *
import tkinter.ttk as ttk
import csv
import datetime
import time
from tkcalendar import DateEntry


def convert_minutes_to_hhmmss(minutes):
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours:02}:{remaining_minutes:02}:00"  # Định dạng hh:mm:ss


def search_attendance(tree, id_entry, date_entry):
    search_id = id_entry.get()
    selected_date = date_entry.get()  # Lấy ngày được chọn

    # Xóa tất cả các mục hiện tại trong bảng
    for item in tree.get_children():
        tree.delete(item)

    # Đọc dữ liệu từ file CSV
    formatted_date = datetime.datetime.strptime(selected_date, "%m/%d/%y").strftime('%d-%m-%Y')
    fileName = f"AttendanceStatistic/AttendanceStatistic_{formatted_date}.csv"

    try:
        with open(fileName) as f:
            reader = csv.DictReader(f, delimiter=',')
            found = False  # Biến kiểm tra xem có tìm thấy ID hay không

            for row in reader:
                if search_id == "" or row['Id'] == search_id:
                    Id = row['Id']
                    Name = row['Name']
                    Date = row['Date']
                    TimeIn = row['Time In']
                    Timeout = row['Time Out']
                    TotalMinutes = int(row['Total time'])  # Giả sử Total time là số phút
                    TotalTime = convert_minutes_to_hhmmss(TotalMinutes)  # Chuyển đổi sang hh:mm:ss
                    tree.insert("", "end", values=(Id, Name, Date, TimeIn, Timeout, TotalTime))
                    found = True

            if not found:
                print("Không tìm thấy ID trong file chấm công cho ngày đã chọn.")
    except FileNotFoundError:
        print("File không tìm thấy.")


def attendance_statistic():
    root = Tk()
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    root.title("Thống kê chấm công ngày " + date)

    # Thiết lập kích thước cửa sổ
    width = 600
    height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(0, 0)

    # Khung chứa tiêu đề
    header_frame = Frame(root, bg='#4CAF50')
    header_frame.pack(fill=X)

    header_label = Label(header_frame, text="Thống Kê Chấm Công", font=("Arial", 20, 'bold'), bg='#4CAF50', fg='white')
    header_label.pack(pady=10)

    # Khung tìm kiếm
    search_frame = Frame(root)
    search_frame.pack(pady=10)

    id_label = Label(search_frame, text="Nhập ID:", font=("Arial", 12))
    id_label.pack(side=LEFT)

    id_entry = Entry(search_frame, font=("Arial", 12))
    id_entry.pack(side=LEFT, padx=5)

    # Ngày chọn
    date_label = Label(search_frame, text="Chọn Ngày:", font=("Arial", 12))
    date_label.pack(side=LEFT, padx=(10, 5))

    date_entry = DateEntry(search_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                           font=("Arial", 12))
    date_entry.pack(side=LEFT)

    search_button = Button(search_frame, text="Tìm Kiếm", font=("Arial", 12),
                           command=lambda: search_attendance(tree, id_entry, date_entry))
    search_button.pack(side=LEFT)

    # Khung chứa bảng
    TableMargin = Frame(root)
    TableMargin.pack(pady=20)

    # Thanh cuộn
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)

    # Bảng
    tree = ttk.Treeview(TableMargin, columns=("Id", "Name", "Date", "Time In", "Time Out", "Total Time"), height=15,
                        selectmode="extended",
                        yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

    # Cấu hình thanh cuộn
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)

    # Tiêu đề bảng
    tree.heading('Id', text="Id", anchor=W)
    tree.heading('Name', text="Name", anchor=W)
    tree.heading('Date', text="Date", anchor=W)
    tree.heading('Time In', text="Time In", anchor=W)
    tree.heading('Time Out', text="Time Out", anchor=W)
    tree.heading('Total Time', text="Total Time", anchor=W)

    # Cấu hình cột
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=50)
    tree.column('#2', stretch=NO, minwidth=0, width=100)
    tree.column('#3', stretch=NO, minwidth=0, width=100)
    tree.column('#4', stretch=NO, minwidth=0, width=100)
    tree.column('#5', stretch=NO, minwidth=0, width=100)

    # Thêm bảng vào khung
    tree.pack()

    # Đọc dữ liệu từ file CSV và thêm vào bảng
    fileName = f"AttendanceStatistic/AttendanceStatistic_{date}.csv"
    try:
        with open(fileName) as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                Id = row['Id']
                Name = row['Name']
                Date = row['Date']
                TimeIn = row['Time In']
                Timeout = row['Time Out']
                Total = row['Total time']
                tree.insert("", "end", values=(Id, Name, Date, TimeIn, Timeout, Total))
    except FileNotFoundError:
        print("File không tìm thấy.")

    # Khởi động giao diện
    root.mainloop()
