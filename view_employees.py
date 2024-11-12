import tkinter as tk
from tkinter import messagebox, ttk
from database import get_employees, update_employee, connect_db

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def view_employees():
    employees = get_employees()  # Lấy thông tin nhân viên từ cơ sở dữ liệu

    if not employees:
        messagebox.showinfo("Thông tin", "Không có nhân viên nào trong cơ sở dữ liệu.")
        return

    view_window = tk.Toplevel()
    view_window.title("Xem Thông Tin Nhân Viên")
    center_window(view_window, 900, 600)  # Căn giữa cửa sổ

    # Tạo bảng để hiển thị thông tin nhân viên
    tree = ttk.Treeview(view_window, columns=("ID", "Tên", "Tuổi", "Giới tính", "Chức vụ", "Phòng ban"), show='headings')
    tree.heading("ID", text="Mã Nhân Viên")
    tree.heading("Tên", text="Tên Nhân Viên")
    tree.heading("Tuổi", text="Tuổi")
    tree.heading("Giới tính", text="Giới Tính")
    tree.heading("Chức vụ", text="Chức Vụ")
    tree.heading("Phòng ban", text="Phòng Ban")

    tree.column("ID", anchor="center", width=100)
    tree.column("Tên", anchor="center", width=150)
    tree.column("Tuổi", anchor="center", width=50)
    tree.column("Giới tính", anchor="center", width=80)
    tree.column("Chức vụ", anchor="center", width=150)
    tree.column("Phòng ban", anchor="center", width=150)

    for employee in employees:
        tree.insert("", tk.END, values=employee)

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    button_frame = tk.Frame(view_window)
    button_frame.pack(pady=10)

    edit_button = tk.Button(button_frame, text="Chỉnh sửa", command=lambda: edit_employee(tree, view_window), bg="#4CAF50", fg="white", width=15)
    edit_button.grid(row=0, column=0, padx=10)

    delete_button = tk.Button(button_frame, text="Xóa", command=lambda: delete_employee(tree), bg="#f44336", fg="white", width=15)
    delete_button.grid(row=0, column=1, padx=10)

def edit_employee(tree, view_window):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên để chỉnh sửa.")
        return

    item = tree.item(selected_item)
    employee_data = item["values"]

    # Khung chỉnh sửa ngay bên dưới bảng hiển thị
    edit_frame = tk.LabelFrame(view_window, text="Chỉnh Sửa Thông Tin Nhân Viên", padx=10, pady=10)
    edit_frame.pack(fill="x", padx=20, pady=10)

    fields = ["ID", "Tên", "Tuổi", "Giới tính", "Chức vụ", "Phòng ban"]
    entries = {}

    for i, field in enumerate(fields):
        tk.Label(edit_frame, text=field).grid(row=i, column=0, padx=10, pady=5, sticky="e")

        if field == "Giới tính":
            gender_combo = ttk.Combobox(edit_frame, values=["Nam", "Nữ"], width=27)
            gender_combo.set(employee_data[i])
            gender_combo.grid(row=i, column=1, padx=10, pady=5)
            entries[field] = gender_combo

        elif field == "Chức vụ":
            position_combo = ttk.Combobox(edit_frame, values=["Nhân viên", "Giám đốc", "Trưởng phòng", "Phó phòng"], width=27)
            position_combo.set(employee_data[i])
            position_combo.grid(row=i, column=1, padx=10, pady=5)
            entries[field] = position_combo

        elif field == "Phòng ban":
            department_combo = ttk.Combobox(edit_frame, values=["Marketing", "Social", "Kỹ thuật", "Hành chính", "Nhân sự", "Biên tập"], width=27)
            department_combo.set(employee_data[i])
            department_combo.grid(row=i, column=1, padx=10, pady=5)
            entries[field] = department_combo

        else:
            entry = tk.Entry(edit_frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, employee_data[i])
            entries[field] = entry

    def save_changes():
        updated_data = {field: entries[field].get() for field in fields}
        success = update_employee(updated_data)
        if success:
            messagebox.showinfo("Thành công", "Thông tin nhân viên đã được cập nhật.")
            view_window.destroy()
            view_employees()  # Tải lại giao diện xem nhân viên để cập nhật dữ liệu
        else:
            messagebox.showerror("Lỗi", "Không thể cập nhật thông tin nhân viên.")

    save_button = tk.Button(edit_frame, text="Lưu Thay Đổi", command=save_changes, bg="#4CAF50", fg="white", width=15)
    save_button.grid(row=len(fields), column=1, pady=10)

def delete_employee(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên để xóa.")
        return

    item = tree.item(selected_item)
    employee_id = item["values"][0]

    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa nhân viên này?")
    if confirm:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM People WHERE ID = ?", (employee_id,))
        conn.commit()
        conn.close()

        tree.delete(selected_item)
        messagebox.showinfo("Thành công", "Nhân viên đã được xóa.")
