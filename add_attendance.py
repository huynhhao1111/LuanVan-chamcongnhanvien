
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import sqlite3
def add_attendance_form():
    add_window = tk.Toplevel()
    add_window.title("Thêm Chấm Công")

    # Nhập ID nhân viên
    tk.Label(add_window, text="ID Nhân Viên:").grid(row=0, column=0)
    id_entry = tk.Entry(add_window)
    id_entry.grid(row=0, column=1)

    # Hiển thị tên nhân viên sau khi nhập ID
    name_label = tk.Label(add_window, text="Tên Nhân Viên:")
    name_label.grid(row=1, column=0)
    name_value = tk.Label(add_window, text="")
    name_value.grid(row=1, column=1)

    # Hàm tìm tên nhân viên từ ID
    def fetch_employee_name():
        person_id = id_entry.get()
        if person_id:
            try:
                conn = sqlite3.connect('FaceBaseNew.db')
                cursor = conn.cursor()
                cursor.execute("SELECT Name FROM People WHERE Id = ?", (person_id,))
                name = cursor.fetchone()
                conn.close()

                if name:
                    name_value.config(text=name[0])  # Hiển thị tên nhân viên
                else:
                    name_value.config(text="Không tìm thấy")
            except sqlite3.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm tên nhân viên: {e}")

    # Gọi hàm tìm tên nhân viên khi nhập ID
    id_entry.bind("<FocusOut>", lambda event: fetch_employee_name())

    # Chọn ngày
    tk.Label(add_window, text="Ngày:").grid(row=2, column=0)
    date_entry = DateEntry(add_window, date_pattern='dd-mm-yyyy')
    date_entry.grid(row=2, column=1)

    # Chọn thời gian vào
    tk.Label(add_window, text="Thời gian vào:").grid(row=3, column=0)
    time_in_hour = ttk.Combobox(add_window, values=[f"{i:02d}" for i in range(24)], width=3)
    time_in_hour.grid(row=3, column=1, padx=(0, 5))
    time_in_minute = ttk.Combobox(add_window, values=[f"{i:02d}" for i in range(0, 60, 5)], width=3)
    time_in_minute.grid(row=3, column=2)
    time_in_hour.set("00")
    time_in_minute.set("00")

    # Chọn thời gian ra
    tk.Label(add_window, text="Thời gian ra:").grid(row=4, column=0)
    time_out_hour = ttk.Combobox(add_window, values=[f"{i:02d}" for i in range(24)], width=3)
    time_out_hour.grid(row=4, column=1, padx=(0, 5))
    time_out_minute = ttk.Combobox(add_window, values=[f"{i:02d}" for i in range(0, 60)], width=3)
    time_out_minute.grid(row=4, column=2)
    time_out_hour.set("00")
    time_out_minute.set("00")

    # Hàm lưu thông tin
    def save_attendance():
        person_id = id_entry.get()
        name = name_value.cget("text")
        date = date_entry.get_date().strftime('%d-%m-%Y')
        time_in = f"{time_in_hour.get()}:{time_in_minute.get()}:00"
        time_out = f"{time_out_hour.get()}:{time_out_minute.get()}:00"

        if not person_id or not date or not time_in or not time_out:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin.")
            return

        try:
            conn = sqlite3.connect('FaceBaseNew.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO AttendanceStatistic (PersonId, Date, TimeIn, TimeOut, TotalTime) VALUES (?, ?, ?, ?, ?)",
                           (person_id, date, time_in, time_out, 0))  # TotalTime sẽ được tính sau
            conn.commit()
            conn.close()
            messagebox.showinfo("Thông báo", "Thêm chấm công thành công.")

            add_window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm dữ liệu: {e}")

    # Nút Lưu
    tk.Button(add_window, text="Lưu", command=save_attendance).grid(row=5, column=0, columnspan=3)

