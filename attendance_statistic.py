import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime
from add_attendance import add_attendance_form  # Import form từ file riêng


# Kết nối đến CSDL
def connect_db():
    conn = sqlite3.connect('FaceBaseNew.db')
    cursor = conn.cursor()
    return conn, cursor


# Hàm tìm kiếm dữ liệu chấm công
def search_attendance(tree, id_entry, date_entry):
    person_id = id_entry.get()
    date = date_entry.get_date().strftime('%d-%m-%Y')

    for row in tree.get_children():
        tree.delete(row)

    conn, cursor = connect_db()
    try:
        query = """
            SELECT a.PersonId, p.Name, a.Date, a.TimeIn, a.TimeOut
            FROM AttendanceStatistic a
            JOIN People p ON a.PersonId = p.ID
        """
        params = []
        if person_id:
            query += " WHERE a.PersonId = ? AND a.Date = ?"
            params = [person_id, date]
        else:
            query += " WHERE a.Date = ?"
            params = [date]

        cursor.execute(query, params)
        rows = cursor.fetchall()

        for row in rows:
            time_in = row[3] if row[3] != '0' else '00:00:00'
            time_out = row[4] if row[4] != '0' else '00:00:00'
            time_in_obj = datetime.strptime(time_in, "%H:%M:%S")
            time_out_obj = datetime.strptime(time_out, "%H:%M:%S")
            total_time = time_out_obj - time_in_obj
            total_hours = int(total_time.total_seconds() // 3600)
            total_minutes = int((total_time.total_seconds() % 3600) // 60)
            total_time_str = f"{total_hours}:{total_minutes:02d}"
            tree.insert('', 'end', values=(row[0], row[1], row[2], time_in, time_out, total_time_str))

        if not rows:
            messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy dữ liệu.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi truy vấn dữ liệu: {e}")
    finally:
        conn.close()


# Hàm xóa thông tin điểm danh
def delete_entry(tree):
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Chọn mục", "Vui lòng chọn một dòng để xóa.")
        return
    values = tree.item(selected_item, 'values')
    person_id, date = values[0], values[2]
    confirm = messagebox.askyesno("Xác nhận xóa",
                                  f"Bạn có chắc chắn muốn xóa thông tin của nhân viên {person_id} vào ngày {date}?")
    if confirm:
        conn, cursor = connect_db()
        try:
            cursor.execute("DELETE FROM AttendanceStatistic WHERE PersonId = ? AND Date = ?", (person_id, date))
            conn.commit()
            tree.delete(selected_item)
            messagebox.showinfo("Thông báo", "Đã xóa thông tin thành công.")
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa dữ liệu: {e}")
        finally:
            conn.close()


# Hàm chỉnh sửa thông tin chấm công
def edit_entry(tree):
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Chọn mục", "Vui lòng chọn một dòng để chỉnh sửa.")
        return
    values = tree.item(selected_item, 'values')
    person_id, date, time_in, time_out = values[0], values[2], values[3], values[4]

    edit_window = tk.Toplevel()
    edit_window.title("Chỉnh sửa thông tin chấm công")
    tk.Label(edit_window, text="Thời gian vào:").grid(row=0, column=0, padx=5, pady=5)
    time_in_entry = tk.Entry(edit_window)
    time_in_entry.insert(0, time_in)
    time_in_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(edit_window, text="Thời gian ra:").grid(row=1, column=0, padx=5, pady=5)
    time_out_entry = tk.Entry(edit_window)
    time_out_entry.insert(0, time_out)
    time_out_entry.grid(row=1, column=1, padx=5, pady=5)

    def save_changes():
        new_time_in, new_time_out = time_in_entry.get(), time_out_entry.get()
        conn, cursor = connect_db()
        try:
            cursor.execute("UPDATE AttendanceStatistic SET TimeIn = ?, TimeOut = ? WHERE PersonId = ? AND Date = ?",
                           (new_time_in, new_time_out, person_id, date))
            conn.commit()
            tree.item(selected_item, values=(person_id, values[1], date, new_time_in, new_time_out, values[5]))
            messagebox.showinfo("Thông báo", "Lưu thay đổi thành công.")
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu thay đổi: {e}")
        finally:
            conn.close()

    tk.Button(edit_window, text="Lưu", command=save_changes).grid(row=2, column=0, columnspan=2, pady=10)


# Giao diện chính
def attendance_statistic():
    root = tk.Tk()
    root.title("Thống Kê Chấm Công")
    root.geometry("900x550")
    root.configure(bg='#f0f0f5')

    # Khung tìm kiếm
    search_frame = tk.Frame(root, bg='#e0e0eb', pady=10)
    search_frame.pack(fill='x', padx=20, pady=10)

    tk.Label(search_frame, text="ID Nhân Viên:", bg='#e0e0eb').grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(search_frame, width=15)
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(search_frame, text="Ngày:", bg='#e0e0eb').grid(row=0, column=2, padx=10, pady=5)
    date_entry = DateEntry(search_frame, date_pattern='y-mm-dd', width=15)
    date_entry.grid(row=0, column=3, padx=10, pady=5)

    search_button = tk.Button(search_frame, text="Tìm Kiếm", bg='#4caf50', fg='white',
                              command=lambda: search_attendance(tree, id_entry, date_entry))
    search_button.grid(row=0, column=4, padx=20, pady=5)

    # Bảng hiển thị kết quả
    columns = ("ID Nhân Viên", "Tên Nhân Viên", "Ngày", "Thời Gian Vào", "Thời Gian Ra", "Tổng Thời Gian")
    tree = ttk.Treeview(root, columns=columns, show='headings', height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(fill='both', expand=True, padx=20, pady=10)

    # Khung chứa các nút
    button_frame = tk.Frame(root, bg='#f0f0f5', pady=10)
    button_frame.pack(fill='x', padx=20, pady=10)

    edit_button = tk.Button(button_frame, text="Chỉnh Sửa", command=lambda: edit_entry(tree), bg='#ffcc00', width=15)
    edit_button.grid(row=0, column=0, padx=10)

    delete_button = tk.Button(button_frame, text="Xóa", command=lambda: delete_entry(tree), bg='#f44336', fg='white',
                              width=15)
    delete_button.grid(row=0, column=1, padx=10)

    add_button = tk.Button(button_frame, text="Thêm Chấm Công", command=add_attendance_form, bg='#2196f3', fg='white',
                           width=15)
    add_button.grid(row=0, column=2, padx=10)

    today = datetime.today().strftime('%Y-%m-%d')
    date_entry.set_date(today)

    search_attendance(tree, id_entry, date_entry)
    root.mainloop()
