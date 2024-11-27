import sqlite3
import tkinter as tk
from tkinter import ttk
import datetime


# Hàm tìm kiếm và sắp xếp điểm danh
def search_attendance(tree, id_entry, status_filter=None):
    search_id = id_entry.get()  # Lấy ID từ ô nhập liệu
    today = datetime.datetime.now().strftime('%d-%m-%Y')  # Lấy ngày hiện tại

    # Xóa tất cả các mục trong bảng
    for item in tree.get_children():
        tree.delete(item)

    try:
        conn = sqlite3.connect('FaceBaseNew.db')
        cursor = conn.cursor()

        query = '''
            SELECT a.Time, a.PersonId, p.Name, a.Status 
            FROM Attendance a
            JOIN People p ON a.PersonId = p.id
            WHERE a.Date = ?
        '''
        params = [today]

        if search_id:
            query += ' AND a.PersonId = ?'
            params.append(search_id)

        if status_filter:
            query += ' AND a.Status = ?'
            params.append(status_filter)

        query += ' ORDER BY a.Time ASC'

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", "end", values=row, tags=('center',))

        conn.close()
    except sqlite3.Error as e:
        print("Lỗi truy vấn cơ sở dữ liệu:", e)


# Hàm tạo giao diện
def attendance():
    root = tk.Tk()
    ts = datetime.datetime.now()
    date = ts.strftime('%d-%m-%Y')
    root.title("Kiểm Tra Chấm Công")
    root.configure(bg='#f7f9fc')

    # Thiết lập kích thước cửa sổ
    width = 950
    height = 650
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(False, False)

    # Tiêu đề
    header_frame = tk.Frame(root, bg='#007BFF')
    header_frame.pack(fill=tk.X)

    header_label = tk.Label(
        header_frame,
        text=f"Kiểm Tra Chấm Công - Ngày {date}",
        font=("Arial", 22, "bold"),
        bg='#007BFF',
        fg='white'
    )
    header_label.pack(pady=10)

    # Khu vực tìm kiếm
    search_frame = tk.Frame(root, bg='#f7f9fc')
    search_frame.pack(pady=15)

    id_label = tk.Label(search_frame, text="Nhập ID:", font=("Arial", 14, "bold"), bg='#f7f9fc')
    id_label.pack(side=tk.LEFT, padx=10)

    id_entry = tk.Entry(search_frame, font=("Arial", 14), width=20)
    id_entry.pack(side=tk.LEFT, padx=10)

    search_button = tk.Button(
        search_frame,
        text="Tìm Kiếm",
        font=("Arial", 14, "bold"),
        bg="#007BFF",
        fg="white",
        activebackground="#0056b3",
        command=lambda: [search_attendance(checkin_tree, id_entry, "In"),
                         search_attendance(checkout_tree, id_entry, "Out")]
    )
    search_button.pack(side=tk.LEFT, padx=10)

    # Tab cho Check In và Check Out
    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, fill=tk.BOTH, expand=True)

    # Tab Check In
    checkin_frame = ttk.Frame(notebook, padding=10)
    notebook.add(checkin_frame, text="Check In")

    checkin_tree = ttk.Treeview(
        checkin_frame,
        columns=("Time", "Id", "Name", "Status"),
        height=15,
        selectmode="extended"
    )
    scrollbary_checkin = tk.Scrollbar(checkin_frame, orient=tk.VERTICAL, command=checkin_tree.yview)
    checkin_tree.configure(yscrollcommand=scrollbary_checkin.set)
    scrollbary_checkin.pack(side=tk.RIGHT, fill=tk.Y)

    checkin_tree.heading('Time', text="Giờ", anchor=tk.CENTER)
    checkin_tree.heading('Id', text="Mã NV", anchor=tk.CENTER)
    checkin_tree.heading('Name', text="Họ Tên", anchor=tk.CENTER)
    checkin_tree.heading('Status', text="Trạng Thái", anchor=tk.CENTER)

    checkin_tree.column('#0', width=0, stretch=tk.NO)
    checkin_tree.column('#1', anchor=tk.CENTER, width=120)
    checkin_tree.column('#2', anchor=tk.CENTER, width=150)
    checkin_tree.column('#3', anchor=tk.CENTER, width=150)
    checkin_tree.column('#4', anchor=tk.CENTER, width=100)

    checkin_tree.pack(fill=tk.BOTH, expand=True)

    # Tab Check Out
    checkout_frame = ttk.Frame(notebook, padding=10)
    notebook.add(checkout_frame, text="Check Out")

    checkout_tree = ttk.Treeview(
        checkout_frame,
        columns=("Time", "Id", "Name", "Status"),
        height=15,
        selectmode="extended"
    )
    scrollbary_checkout = tk.Scrollbar(checkout_frame, orient=tk.VERTICAL, command=checkout_tree.yview)
    checkout_tree.configure(yscrollcommand=scrollbary_checkout.set)
    scrollbary_checkout.pack(side=tk.RIGHT, fill=tk.Y)

    checkout_tree.heading('Time', text="Giờ", anchor=tk.CENTER)
    checkout_tree.heading('Id', text="Mã NV", anchor=tk.CENTER)
    checkout_tree.heading('Name', text="Họ Tên", anchor=tk.CENTER)
    checkout_tree.heading('Status', text="Trạng Thái", anchor=tk.CENTER)

    checkout_tree.column('#0', width=0, stretch=tk.NO)
    checkout_tree.column('#1', anchor=tk.CENTER, width=120)
    checkout_tree.column('#2', anchor=tk.CENTER, width=150)
    checkout_tree.column('#3', anchor=tk.CENTER, width=150)
    checkout_tree.column('#4', anchor=tk.CENTER, width=100)

    checkout_tree.pack(fill=tk.BOTH, expand=True)

    # Hiển thị dữ liệu ban đầu
    search_attendance(checkin_tree, id_entry, "In")
    search_attendance(checkout_tree, id_entry, "Out")

    root.mainloop()

