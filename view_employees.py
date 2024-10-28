import tkinter as tk
from tkinter import messagebox, ttk
from database import get_employees

def view_employees():
    employees = get_employees()  # Lấy thông tin nhân viên từ cơ sở dữ liệu

    if not employees:
        messagebox.showinfo("Thông tin", "Không có nhân viên nào trong cơ sở dữ liệu.")
        return

    view_window = tk.Toplevel()
    view_window.title("Xem Thông Tin Nhân Viên")
    view_window.geometry("600x400")

    # Tạo bảng để hiển thị thông tin nhân viên
    tree = ttk.Treeview(view_window, columns=("ID", "Tên", "Chức vụ", "Phòng ban", "Email", "Số điện thoại"), show='headings')
    tree.heading("ID", text="Mã Nhân Viên")
    tree.heading("Tên", text="Tên Nhân Viên")
    tree.heading("Chức vụ", text="Chức Vụ")
    tree.heading("Phòng ban", text="Phòng Ban")
    tree.heading("Email", text="Email")
    tree.heading("Số điện thoại", text="Số Điện Thoại")

    # Chèn dữ liệu vào bảng
    for employee in employees:
        tree.insert("", tk.END, values=employee)

    tree.pack(fill=tk.BOTH, expand=True)

    # Tạo thanh cuộn
    scrollbar = ttk.Scrollbar(view_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

