import sqlite3
import tkinter as tk
from tkinter import ttk
from datetime import datetime


# Kết nối đến cơ sở dữ liệu
def connect_database(db_name):
    conn = sqlite3.connect(db_name)
    return conn


# Lấy danh sách nhân viên từ bảng People
def get_people_data(conn):
    query = "SELECT ID, Name FROM People"
    return conn.execute(query).fetchall()


# Lấy dữ liệu chấm công từ bảng AttendanceStatistic
def get_attendance_data(conn, person_id, month, year):
    query = f"""
    SELECT Date, TimeIn, TimeOut, TotalTime
    FROM AttendanceStatistic
    WHERE PersonId = ? AND strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
    """
    return conn.execute(query, (person_id, f"{month:02d}", str(year))).fetchall()


# Hàm hiển thị dữ liệu chấm công lên bảng
def view_data(tree, conn, month, year, employee_id):
    # Xóa dữ liệu cũ trong TreeView
    for item in tree.get_children():
        tree.delete(item)

    # Lấy dữ liệu chấm công
    if employee_id == "all":
        employee_query = "SELECT ID, Name FROM People"
        employees = conn.execute(employee_query).fetchall()
    else:
        employee_query = "SELECT ID, Name FROM People WHERE ID = ?"
        employees = conn.execute(employee_query, (employee_id,)).fetchall()

    for emp in employees:
        person_id, name = emp
        attendance = get_attendance_data(conn, person_id, month, year)
        total_days = len(attendance)
        total_hours = sum(row[3] for row in attendance)

        # Hiển thị từng nhân viên trong bảng
        row_data = [name]
        for date, time_in, time_out, total_time in attendance:
            day = datetime.strptime(date, '%Y-%m-%d').day
            row_data.append(f"{day}: {total_time}h")
        row_data.append(total_days)
        row_data.append(total_hours)
        tree.insert("", "end", values=row_data)


# Xây dựng giao diện
def create_interface(db_name):
    # Kết nối cơ sở dữ liệu
    conn = connect_database(db_name)

    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("Chấm Công và Tính Lương")
    root.geometry("1200x700")
    root.configure(bg="#f5f5f5")

    # Khung chọn thông tin
    filter_frame = tk.Frame(root, bg="#e0e0eb", padx=10, pady=10)
    filter_frame.pack(fill="x", padx=10, pady=10)

    tk.Label(filter_frame, text="Chọn Nhân Viên:", bg="#e0e0eb").grid(row=0, column=0, padx=5, pady=5)
    employee_combo = ttk.Combobox(filter_frame, width=20)
    employee_data = get_people_data(conn)
    employee_combo["values"] = ["Tất cả"] + [f"{emp[0]} - {emp[1]}" for emp in employee_data]
    employee_combo.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(filter_frame, text="Tháng:", bg="#e0e0eb").grid(row=0, column=2, padx=5, pady=5)
    month_combo = ttk.Combobox(filter_frame, width=10)
    month_combo["values"] = [f"{i}" for i in range(1, 13)]
    month_combo.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(filter_frame, text="Năm:", bg="#e0e0eb").grid(row=0, column=4, padx=5, pady=5)
    year_combo = ttk.Combobox(filter_frame, width=10)
    year_combo["values"] = [str(y) for y in range(2020, 2030)]
    year_combo.grid(row=0, column=5, padx=5, pady=5)

    view_button = tk.Button(filter_frame, text="Xem Dữ Liệu", bg="#4caf50", fg="white",
                            command=lambda: view_data(attendance_tree, conn, int(month_combo.get()),
                                                      int(year_combo.get()),
                                                      "all" if employee_combo.get() == "Tất cả" else
                                                      employee_combo.get().split(" - ")[0]))
    view_button.grid(row=0, column=6, padx=10, pady=5)

    # Bảng hiển thị chấm công
    columns = ["Tên Nhân Viên"] + [f"Ngày {i}" for i in range(1, 32)] + ["Tổng Ngày", "Tổng Giờ"]
    attendance_tree = ttk.Treeview(root, columns=columns, show="headings", height=20)

    for col in columns:
        attendance_tree.heading(col, text=col)
        attendance_tree.column(col, width=100 if "Ngày" in col else 150, anchor="center")

    attendance_tree.pack(fill="both", expand=True, padx=10, pady=10)

    root.mainloop()


# Gọi hàm để chạy ứng dụng
create_interface("FaceBaseNew.db")
