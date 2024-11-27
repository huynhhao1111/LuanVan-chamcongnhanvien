import os
import shutil
import tkinter as tk
from dbm import error
from tkinter import messagebox, ttk
from database import get_employees, update_employee, connect_db
import unicodedata
import re

def format_name_to_encoding(name, employee_id):
    # Chuyển đổi thành không dấu
    name_without_accent = ''.join(
        (c for c in unicodedata.normalize("NFD", name) if unicodedata.category(c) != "Mn")
    )
    # Thay khoảng trắng bằng dấu gạch dưới
    formatted_name = re.sub(r"\s+", "_", name_without_accent.strip())
    # Thêm ID vào cuối
    return f"{formatted_name}_{employee_id}"

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
def ask_yes_no(title, message):
    """
    Tạo một cửa sổ hỏi xác nhận (Yes/No) với thiết kế đẹp hơn.
    :param title: Tiêu đề của cửa sổ.
    :param message: Nội dung câu hỏi.
    :return: True nếu chọn "Yes", False nếu chọn "No".
    """
    result = {"value": None}

    def on_yes():
        result["value"] = True
        confirm_window.destroy()

    def on_no():
        result["value"] = False
        confirm_window.destroy()

    # Tạo cửa sổ Toplevel
    confirm_window = tk.Toplevel()
    confirm_window.title(title)

    # Kích thước cửa sổ
    window_width = 350
    window_height = 200

    # Lấy kích thước màn hình
    screen_width = confirm_window.winfo_screenwidth()
    screen_height = confirm_window.winfo_screenheight()

    # Tính toán tọa độ để canh giữa
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)

    # Đặt vị trí và kích thước cửa sổ
    confirm_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    confirm_window.resizable(False, False)
    confirm_window.grab_set()  # Chặn thao tác bên ngoài cửa sổ này

    # Tạo nền và thêm viền
    confirm_window.configure(bg="#f0f8ff")  # Màu nền nhạt (AliceBlue)

    # Tiêu đề thông báo
    tk.Label(
        confirm_window,
        text=title,
        font=("Arial", 14, "bold"),
        fg="#2f4f4f",  # Màu chữ (Dark Slate Gray)
        bg="#f0f8ff",
        pady=10
    ).pack()

    # Nội dung thông báo
    tk.Label(
        confirm_window,
        text=message,
        font=("Arial", 12),
        wraplength=320,
        fg="#333333",  # Màu chữ (Gray)
        bg="#f0f8ff",
        padx=20,
        pady=10
    ).pack()

    # Khung nút bấm
    button_frame = tk.Frame(confirm_window, bg="#f0f8ff")
    button_frame.pack(pady=20)

    # Nút "Có" (Yes)
    tk.Button(
        button_frame,
        text="Có",
        width=12,
        bg="#32cd32",  # Màu xanh lá (Lime Green)
        fg="white",
        font=("Arial", 10, "bold"),
        command=on_yes
    ).grid(row=0, column=0, padx=10)

    # Nút "Không" (No)
    tk.Button(
        button_frame,
        text="Không",
        width=12,
        bg="#dc143c",  # Màu đỏ (Crimson)
        fg="white",
        font=("Arial", 10, "bold"),
        command=on_no
    ).grid(row=0, column=1, padx=10)

    # Chờ cửa sổ đóng và trả kết quả
    confirm_window.wait_window()
    return result["value"]
import pickle

def delete_person_encoding(encodings_file, person_name):
    # Tải dữ liệu mã hóa hiện tại
    with open(encodings_file, "rb") as f:
        data = pickle.load(f)

    encodings = data.get("encodings", [])
    names = data.get("names", [])

    # Lọc bỏ dữ liệu của người cần xóa
    filtered_encodings = []
    filtered_names = []
    for encoding, name in zip(encodings, names):
        if name != person_name:
            filtered_encodings.append(encoding)
            filtered_names.append(name)

    # Ghi đè lại file encodings.pickle
    updated_data = {"encodings": filtered_encodings, "names": filtered_names}
    with open(encodings_file, "wb") as f:
        f.write(pickle.dumps(updated_data))

    print(f"[INFO] Đã xóa dữ liệu của {person_name}.")

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def view_employees():
    employees = get_employees()  # Lấy thông tin nhân viên từ cơ sở dữ liệu

    if not employees:
        show_message("Thông tin", "Không có nhân viên nào trong cơ sở dữ liệu.", "info")
        return

    view_window = tk.Toplevel()
    view_window.title("Xem Thông Tin Nhân Viên")
    center_window(view_window, 900, 650)  # Căn giữa cửa sổ

    # Khung chọn phòng ban
    filter_frame = tk.Frame(view_window)
    filter_frame.pack(pady=10)

    tk.Label(filter_frame, text="Chọn Phòng Ban:", font=("Arial", 12)).grid(row=0, column=0, padx=10)

    department_combo = ttk.Combobox(
        filter_frame,
        values=["Tất cả", "Marketing", "Social", "Kỹ thuật", "Hành chính", "Nhân sự", "Biên tập"],
        width=27,
    )
    department_combo.set("Tất cả")
    department_combo.grid(row=0, column=1, padx=10)

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

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Hàm để cập nhật bảng theo phòng ban
    def filter_employees():
        selected_department = department_combo.get()
        filtered_employees = []

        if selected_department == "Tất cả":
            filtered_employees = employees
        else:
            filtered_employees = [emp for emp in employees if emp[5] == selected_department]

        # Xóa dữ liệu cũ trong bảng
        tree.delete(*tree.get_children())

        # Chèn dữ liệu mới
        for employee in filtered_employees:
            tree.insert("", tk.END, values=employee)

    # Nút lọc dữ liệu
    filter_button = tk.Button(filter_frame, text="Lọc", command=filter_employees, bg="#4CAF50", fg="white", width=10)
    filter_button.grid(row=0, column=2, padx=10)

    # Hiển thị toàn bộ dữ liệu mặc định
    for employee in employees:
        tree.insert("", tk.END, values=employee)

    button_frame = tk.Frame(view_window)
    button_frame.pack(pady=10)

    edit_button = tk.Button(button_frame, text="Chỉnh sửa", command=lambda: edit_employee(tree, view_window), bg="#4CAF50", fg="white", width=15)
    edit_button.grid(row=0, column=0, padx=10)

    delete_button = tk.Button(button_frame, text="Xóa", command=lambda: delete_employee(tree), bg="#f44336", fg="white", width=15)
    delete_button.grid(row=0, column=1, padx=10)

def edit_employee(tree, view_window):
    selected_item = tree.selection()
    if not selected_item:
        show_message("Cảnh báo", "Vui lòng chọn một nhân viên để chỉnh sửa.", "warning")
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
            show_message("Thành công", "Thông tin nhân viên đã được cập nhật.", "info")
            # view_window.destroy()
        else:
            show_message("Lỗi", "Không thể cập nhật thông tin nhân viên.", "error")
        # view_employees()  # Tải lại giao diện xem nhân viên để cập nhật dữ liệu

    save_button = tk.Button(edit_frame, text="Lưu Thay Đổi", command=save_changes, bg="#4CAF50", fg="white", width=15)
    save_button.grid(row=len(fields), column=1, pady=10)

def delete_employee(tree):
    selected_item = tree.selection()
    if not selected_item:
        show_message("Cảnh báo", "Vui lòng chọn một nhân viên để xóa.", "warning")
        return

    item = tree.item(selected_item)
    employee_id = item["values"][0]  # ID nhân viên
    employee_name = item["values"][1]  # Tên nhân viên

    # Chuyển đổi tên thành dạng chuẩn hóa
    formatted_name = format_name_to_encoding(employee_name, employee_id)
    # Thư mục chứa hình ảnh training của nhân viên
    folder_name = f"TrainingImage/{formatted_name}"
    # Xác nhận xóa
    confirm = ask_yes_no("Xác nhận", "Bạn có chắc muốn xóa nhân viên này?")
    if confirm:
        # Xóa dữ liệu trong cơ sở dữ liệu
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM People WHERE ID = ?", (employee_id,))
        conn.commit()
        conn.close()

        # Xóa nhân viên khỏi treeview
        tree.delete(selected_item)
        # Xóa thư mục chứa dữ liệu training (nếu tồn tại)
        if os.path.exists(folder_name):
            try:
                shutil.rmtree(folder_name)
                print(f"Đã xóa thư mục: {folder_name}")
            except Exception as e:
                show_message("Lỗi", f"Không thể xóa thư mục: {str(e)}", error)
        # Xóa dữ liệu mã hóa
        delete_person_encoding("encodings/encodings.pickle", formatted_name)

        show_message("Thành công", "Nhân viên đã được xóa.", "info")
