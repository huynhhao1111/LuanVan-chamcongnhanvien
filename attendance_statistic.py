import csv
import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime, timedelta
from add_attendance import add_attendance_form  # Import form từ file riêng


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


# Kết nối đến CSDL
def connect_db():
    conn = sqlite3.connect('FaceBaseNew.db')
    cursor = conn.cursor()
    return conn, cursor


# Hàm tìm kiếm dữ liệu chấm công

from datetime import datetime, timedelta
import sqlite3

def search_attendance(tree, id_entry, start_date_entry, end_date_entry):
    person_id = id_entry.get()
    start_date = start_date_entry.get_date().strftime('%Y-%m-%d')  # Lấy ngày từ DateEntry
    end_date = end_date_entry.get_date().strftime('%Y-%m-%d')  # Lấy ngày từ DateEntry

    for row in tree.get_children():
        tree.delete(row)

    conn, cursor = connect_db()

    try:

        query = """
            SELECT a.Date, a.PersonId, p.Name, a.TimeIn, a.TimeOut
            FROM AttendanceStatistic a
            JOIN People p ON a.PersonId = p.ID
            WHERE STRFTIME('%Y-%m-%d', SUBSTR(a.Date, 7, 4) || '-' || SUBSTR(a.Date, 4, 2) || '-' || SUBSTR(a.Date, 1, 2))
            BETWEEN ? AND ?
        """
        params = [start_date, end_date]

        if person_id:
            query += " AND a.PersonId = ?"
            params.append(person_id)

        query += " ORDER BY STRFTIME('%Y-%m-%d', SUBSTR(a.Date, 7, 4) || '-' || SUBSTR(a.Date, 4, 2) || '-' || SUBSTR(a.Date, 1, 2))"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        # Lấy danh sách tất cả nhân viên để kiểm tra xem ai chưa có điểm danh
        cursor.execute("SELECT id FROM People")
        all_employees = cursor.fetchall()

        # Kiểm tra mỗi nhân viên trong khoảng thời gian đã chọn
        for employee in all_employees:
            person_id = employee[0]
            current_date = datetime.strptime(start_date, '%Y-%m-%d')  # Chuyển start_date sang đối tượng datetime

            while current_date <= datetime.strptime(end_date, '%Y-%m-%d'):  # So sánh với end_date
                formatted_date = current_date.strftime('%d-%m-%Y')  # Định dạng ngày là %d-%m-%Y

                # Kiểm tra xem nhân viên đã có điểm danh chưa
                cursor.execute("SELECT * FROM AttendanceStatistic WHERE PersonId = ? AND Date = ?",
                               (person_id, formatted_date))
                if not cursor.fetchone():  # Nếu chưa có, chèn bản ghi mới
                    cursor.execute("""
                                INSERT INTO AttendanceStatistic (PersonId, Date, TimeIn, TimeOut, TotalTime)
                                VALUES (?, ?, '00:00:00', '00:00:00', 0)
                            """, (person_id, formatted_date))

                # Cộng thêm một ngày vào current_date
                current_date = current_date + timedelta(days=1)

        for row in rows:
            time_in = row[3]
            time_out = row[4]
            formatted_date = datetime.strptime(row[0], "%d-%m-%Y").strftime('%Y-%m-%d')
            print(formatted_date)
            if time_in == '00:00:00' and time_out == '00:00:00':  # Cả TimeIn và TimeOut đều là 0
                cursor.execute("SELECT LeaveType FROM Leave WHERE PersonId = ? AND Date= ?", (row[1], formatted_date))
                leave_info = cursor.fetchone()
                print(leave_info)
                if leave_info:
                    status = f"Nghỉ Phép ({leave_info[0]})"
                else:
                    status = "Không Phép"
                total_time_str = '00:00'
                ot_time_str = '00:00'
            elif time_in != '00:00:00' and time_out == '00:00:00':  # TimeIn có giá trị, TimeOut = 0
                status = "Quên Check Out"
                total_time_str = '00:00'
                ot_time_str = '00:00'
            else:
                time_in_obj = datetime.strptime(time_in, "%H:%M:%S")
                time_out_obj = datetime.strptime(time_out, "%H:%M:%S")
                total_time = time_out_obj - time_in_obj
                total_hours = int(total_time.total_seconds() // 3600)
                total_minutes = int((total_time.total_seconds() % 3600) // 60)
                total_time_str = f"{total_hours}:{total_minutes:02d}"
                status = "Đi Làm" if total_time.total_seconds() > 0 else "Quên Check Out"

                ot_seconds = max(0, total_time.total_seconds() - 8 * 3600)
                ot_hours = int(ot_seconds // 3600)
                ot_minutes = int((ot_seconds % 3600) // 60)
                ot_time_str = f"{ot_hours}:{ot_minutes:02d}"

            row_id = tree.insert('', 'end', values=(row[0], row[1], row[2], time_in, time_out, total_time_str, ot_time_str, status))

            # Tô màu nếu cần thiết
            if "Phép" in status:
                tree.tag_configure('absent', background='#ffcccc')  # Màu đỏ nhạt
                tree.item(row_id, tags='absent')
            elif status == "Quên Check Out":
                tree.tag_configure('warning', background='#fff0b3')  # Màu vàng nhạt
                tree.item(row_id, tags='warning')

        if not rows:
            show_message("Kết quả tìm kiếm", "Không tìm thấy dữ liệu.", "info")
        conn.commit()

    except Exception as e:
        show_message("Lỗi", f"Lỗi khi truy vấn dữ liệu: {e}", "error")
    finally:
        conn.close()


# Hàm xóa thông tin điểm danh
def delete_entry(tree):
    selected_item = tree.focus()
    if not selected_item:
        show_message("Chọn mục", "Vui lòng chọn một dòng để xóa.", "info")
        return
    values = tree.item(selected_item, 'values')
    person_id, date, name = values[1], values[0], values[2]

    def confirm_delete():
        conn, cursor = connect_db()
        try:
            cursor.execute("DELETE FROM AttendanceStatistic WHERE PersonId = ? AND Date = ?", (person_id, date))
            cursor.execute("DELETE FROM Attendance WHERE PersonId = ? AND Date = ?", (person_id, date))
            conn.commit()
            tree.delete(selected_item)
            show_message("Thông báo", "Đã xóa thông tin thành công.", "info")
        except sqlite3.Error as e:
            show_message("Lỗi", f"Lỗi khi xóa dữ liệu: {e}", "error")
        finally:
            conn.close()

    confirm_window = tk.Toplevel()
    confirm_window.title("Xác nhận xóa")
    confirm_window.geometry("300x200")
    confirm_window.resizable(False, False)

    # Căn giữa cửa sổ Xác nhận xóa
    screen_width = confirm_window.winfo_screenwidth()
    screen_height = confirm_window.winfo_screenheight()
    window_width = 300
    window_height = 200
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    confirm_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Thêm màu nền và căn chỉnh văn bản
    confirm_window.config(bg="#f0f8ff")

    # Sử dụng Frame để căn chỉnh nội dung
    frame = tk.Frame(confirm_window, bg="#f0f8ff")
    frame.pack(pady=20)

    # Thêm label cho nội dung xác nhận
    label = tk.Label(frame, text=f"Bạn có chắc chắn muốn xóa thông tin của nhân viên {name} vào ngày {date}?",
                     wraplength=260, font=("Arial", 10), bg="#f0f8ff")
    label.pack(pady=10)

    # Thêm các nút với style đẹp hơn
    button_frame = tk.Frame(confirm_window, bg="#f0f8ff")
    button_frame.pack(pady=10)

    yes_button = tk.Button(button_frame, text="Có", command=lambda: [confirm_window.destroy(), confirm_delete()],
                           width=12, height=2, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
    yes_button.pack(side="left", padx=10)

    no_button = tk.Button(button_frame, text="Không", command=confirm_window.destroy,
                          width=12, height=2, bg="#f44336", fg="white", font=("Arial", 10, "bold"))
    no_button.pack(side="right", padx=10)

# Hàm chỉnh sửa thông tin chấm công
# Hàm chỉnh sửa thông tin chấm công
def edit_entry(tree, id_entry, start_date_entry, end_date_entry):
    selected_item = tree.focus()
    if not selected_item:
        show_message("Chọn mục", "Vui lòng chọn một dòng để chỉnh sửa.", "warning")
        return
    values = tree.item(selected_item, 'values')
    person_id, date, time_in, time_out = values[1], values[0], values[3], values[4]

    # Tạo cửa sổ chỉnh sửa
    edit_window = tk.Toplevel()
    edit_window.title("Chỉnh sửa thông tin chấm công")
    edit_window.resizable(False, False)

    # Kích thước cửa sổ
    window_width = 300
    window_height = 200

    # Lấy kích thước màn hình
    screen_width = edit_window.winfo_screenwidth()
    screen_height = edit_window.winfo_screenheight()

    # Tính toán tọa độ để canh giữa
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)

    # Đặt vị trí cửa sổ
    edit_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Label và Entry cho "Thời gian vào"
    tk.Label(edit_window, text="Thời gian vào:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    time_in_entry = tk.Entry(edit_window, font=("Arial", 12))
    time_in_entry.insert(0, time_in)
    time_in_entry.grid(row=0, column=1, padx=10, pady=10)

    # Label và Entry cho "Thời gian ra"
    tk.Label(edit_window, text="Thời gian ra:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    time_out_entry = tk.Entry(edit_window, font=("Arial", 12))
    time_out_entry.insert(0, time_out)
    time_out_entry.grid(row=1, column=1, padx=10, pady=10)

    # Hàm lưu thay đổi
    def save_changes():
        new_time_in = time_in_entry.get()
        new_time_out = time_out_entry.get()

        # Chuẩn hóa giá trị new_time_out
        if new_time_out in ["0", "00:00", "00:00:00"]:
            new_time_out = "00:00:00"

        conn, cursor = connect_db()
        try:
            # Cập nhật AttendanceStatistic
            cursor.execute(
                "UPDATE AttendanceStatistic SET TimeIn = ?, TimeOut = ? WHERE PersonId = ? AND Date = ?",
                (new_time_in, new_time_out, person_id, date)
            )

            # Cập nhật trạng thái "IN"
            cursor.execute(
                "SELECT * FROM Attendance WHERE PersonId = ? AND Date = ? AND Status = 'In'",
                (person_id, date)
            )
            if cursor.fetchone():
                # Nếu đã tồn tại, cập nhật
                cursor.execute(
                    "UPDATE Attendance SET Time = ? WHERE PersonId = ? AND Date = ? AND Status = 'In'",
                    (new_time_in, person_id, date)
                )
            else:
                # Nếu không tồn tại, tạo mới
                cursor.execute(
                    "INSERT INTO Attendance (PersonId, Date, Time, Status) VALUES (?, ?, ?, 'In')",
                    (person_id, date, new_time_in)
                )

            # Cập nhật trạng thái "OUT"
            cursor.execute(
                "SELECT * FROM Attendance WHERE PersonId = ? AND Date = ? AND Status = 'Out'",
                (person_id, date)
            )
            existing_out = cursor.fetchone()

            if new_time_out == "00:00:00":
                # Nếu giá trị mới là "00:00:00" và OUT đã tồn tại, xóa dòng OUT
                if existing_out:
                    cursor.execute(
                        "DELETE FROM Attendance WHERE PersonId = ? AND Date = ? AND Status = 'Out'",
                        (person_id, date)
                    )
            else:
                # Nếu OUT không phải "00:00:00", cập nhật hoặc thêm mới
                if existing_out:
                    cursor.execute(
                        "UPDATE Attendance SET Time = ? WHERE PersonId = ? AND Date = ? AND Status = 'Out'",
                        (new_time_out, person_id, date)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO Attendance (PersonId, Date, Time, Status) VALUES (?, ?, ?, 'Out')",
                        (person_id, date, new_time_out)
                    )

            # Lưu thay đổi vào CSDL
            conn.commit()

            # Làm mới bảng hiển thị
            search_attendance(tree, id_entry, start_date_entry, end_date_entry)

            show_message("Thông báo", "Lưu thay đổi thành công.", "info")
            edit_window.destroy()  # Đóng cửa sổ sau khi lưu thành công
        except sqlite3.Error as e:
            show_message("Lỗi", f"Lỗi khi lưu thay đổi: {e}", "error")
        finally:
            conn.close()

    # Nút "Lưu"
    save_button = tk.Button(edit_window, text="Lưu", command=save_changes, bg="#4caf50", fg="white", font=("Arial", 12))
    save_button.grid(row=2, column=0, columnspan=2, pady=15)

    # Căn chỉnh layout
    for i in range(2):
        edit_window.grid_columnconfigure(i, weight=1)



import pandas as pd  # Dùng để xuất dữ liệu ra file Excel hoặc CSV




# Hàm preview_and_export_data đã sửa lại
def preview_and_export_data(tree, id_entry, start_date_entry, end_date_entry):
    # Kiểm tra nếu `tree` đã có dữ liệu
    rows = []
    for item in tree.get_children():
        rows.append(tree.item(item, 'values'))

    if not rows:
        show_message("Thông báo", "Không có dữ liệu để xuất.", "info")
        return

    # Hiển thị cửa sổ kiểm tra dữ liệu
    preview_window = tk.Toplevel()
    preview_window.title("Xem Trước Dữ Liệu")

    # Tính toán vị trí căn giữa
    screen_width = preview_window.winfo_screenwidth()
    screen_height = preview_window.winfo_screenheight()
    window_width = 1000
    window_height = 550
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)

    preview_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    preview_window.resizable(True, True)

    # Tạo bảng hiển thị dữ liệu
    columns = (
        "Ngày", "ID Nhân Viên", "Tên Nhân Viên", "Thời Gian Vào", "Thời Gian Ra", "Tổng Thời Gian", "Giờ Làm Thêm",
        "Trạng Thái")
    preview_tree = ttk.Treeview(preview_window, columns=columns, show='headings', height=15)

    for col in columns:
        preview_tree.heading(col, text=col)
        preview_tree.column(col, anchor="center", width=120)

    preview_tree.pack(fill='both', expand=True, padx=20, pady=10)

    # Thêm dữ liệu vào bảng `preview_tree`
    for row in rows:
        preview_tree.insert('', 'end', values=row)

    # Nút xuất dữ liệu ra Excel hoặc CSV
    def export_data():
        data = []
        for row in rows:
            data.append(row)

        # Xuất dữ liệu ra file CSV
        export_to_csv(data, columns)

    export_button = tk.Button(preview_window, text="Xuất Dữ Liệu", command=export_data)
    export_button.pack(pady=10)

def export_to_csv(data, columns):
    # Chọn vị trí lưu file
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    # Ghi dữ liệu vào file
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # Ghi tiêu đề
        writer.writerows(data)  # Ghi nội dung

    show_message("Thông báo", "Dữ liệu đã được xuất thành công.", "info")

def attendance_statistic():
    root = tk.Tk()
    root.title("Điều Chỉnh Thông Tin Chấm Công")

    window_width = 1000
    window_height = 550
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)

    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    root.configure(bg='#f0f0f5')

    search_frame = tk.Frame(root, bg='#e0e0eb', pady=10)
    search_frame.pack(fill='x', padx=10, pady=10)

    tk.Label(search_frame, text="ID Nhân Viên:", bg='#e0e0eb').grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(search_frame, width=15)
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(search_frame, text="Ngày Bắt Đầu:", bg='#e0e0eb').grid(row=0, column=2, padx=10, pady=5)
    start_date_entry = DateEntry(search_frame, date_pattern='dd-mm-yyyy', width=15)
    start_date_entry.grid(row=0, column=3, padx=10, pady=5)

    tk.Label(search_frame, text="Ngày Kết Thúc:", bg='#e0e0eb').grid(row=0, column=4, padx=10, pady=5)
    end_date_entry = DateEntry(search_frame, date_pattern='dd-mm-yyyy', width=15)
    end_date_entry.grid(row=0, column=5, padx=10, pady=5)

    search_button = tk.Button(search_frame, text="Tìm Kiếm", bg='#4caf50', fg='white',
                              command=lambda: search_attendance(tree, id_entry, start_date_entry, end_date_entry))
    search_button.grid(row=0, column=6, padx=10, pady=5)


    # Bảng hiển thị kết quả
    columns = (
    "Ngày", "ID Nhân Viên", "Tên Nhân Viên", "Thời Gian Vào", "Thời Gian Ra", "Tổng Thời Gian", "Giờ Làm Thêm","Trạng Thái")
    tree = ttk.Treeview(root, columns=columns, show='headings', height=15)

    # Cấu hình các cột cho bảng
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)  # Đảm bảo các cột không bị tràn
    tree.pack(fill='both', expand=True, padx=20, pady=10)

    # Khung chứa các nút
    button_frame = tk.Frame(root, bg='#f0f0f5', pady=20)
    button_frame.pack(fill='x', padx=20, pady=10)

    # Các nút bấm với màu sắc và kiểu dáng đẹp mắt
    edit_button = tk.Button(button_frame, text="Chỉnh Sửa", bg='#2196f3', fg='white',
                            font=("Arial", 10, "bold"),
                            command=lambda: edit_entry(tree, id_entry, start_date_entry, end_date_entry))
    edit_button.grid(row=0, column=0, padx=10, pady=10, ipadx=15, ipady=10)

    delete_button = tk.Button(button_frame, text="Xóa", command=lambda: delete_entry(tree), bg='#f44336', fg='white',
                              font=("Arial", 10, "bold"), width=10)
    delete_button.grid(row=0, column=1, padx=10, pady=10, ipadx=15, ipady=10)

    add_button = tk.Button(button_frame, text="Thêm Chấm Công", command=add_attendance_form, bg='#2196f3', fg='white',
                           font=("Arial", 10, "bold"), width=10)
    add_button.grid(row=0, column=2, padx=10, pady=10, ipadx=15, ipady=10)

    export_button = tk.Button(button_frame, text="Xuất Báo Cáo", bg="#2196f3", fg="white", font=("Arial", 10, "bold"),
                              command=lambda: preview_and_export_data(tree, id_entry, start_date_entry, end_date_entry))
    export_button.grid(row=0, column=3, padx=10, pady=10, ipadx=15, ipady=10)

    # Căn giữa các nút trong button_frame
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1)
    button_frame.grid_columnconfigure(3, weight=1)

    # Đặt ngày hiện tại vào date_entry
    # Chuyển đổi ngày theo định dạng 'yyyy-mm-dd' thành đối tượng datetime.date
    today = datetime.today().date()
    print(today)  # Kiểm tra giá trị của 'today'

    # Đặt ngày vào DateEntry
    start_date_entry.set_date(today)
    end_date_entry.set_date(today)

    # Gọi hàm tìm kiếm mặc định để hiển thị dữ liệu
    # search_attendance(tree, id_entry, start_date_entry, end_date_entry)

    root.mainloop()
