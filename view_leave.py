import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from database import get_leaves, connect_db, get_employee_name, add_leave  # Giả định bạn đã định nghĩa các hàm này
from datetime import datetime

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

def show_message(title, message, message_type="info"):
    # Định nghĩa màu nền theo loại thông báo
    colors = {
        "info": "#d4edda",      # Xanh lá nhạt
        "error": "#f8d7da",     # Đỏ nhạt
        "warning": "#fff3cd",   # Vàng nhạt
        "default": "#d1ecf1"    # Xanh dương nhạt
    }

    # Lấy màu nền từ loại thông báo, nếu không có thì dùng "default"
    background_color = colors.get(message_type, colors["default"])
    text_color = "black"

    # Tạo cửa sổ con
    window = tk.Toplevel()
    window.title(title)
    window.configure(bg=background_color)

    # Kích thước cửa sổ
    window_width = 300
    window_height = 150

    # Lấy kích thước màn hình
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Tính toán tọa độ để canh giữa
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)

    # Đặt vị trí và kích thước cửa sổ
    window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    window.resizable(False, False)

    # Thêm các widget
    tk.Label(
        window,
        text=title,
        font=("Arial", 14, "bold"),
        fg=text_color,
        bg=background_color
    ).pack(pady=10)

    tk.Label(
        window,
        text=message,
        font=("Arial", 12),
        wraplength=280,
        fg=text_color,
        bg=background_color
    ).pack(pady=10)

    tk.Button(
        window,
        text="Đóng",
        command=window.destroy,
        bg="white",
        fg="black"
    ).pack(pady=10)

    # Làm cho cửa sổ trở thành cửa sổ con
    window.transient()
    window.grab_release()

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


def search_leave_in_range():
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()
    employee_id = id_entry.get()

    if start_date > end_date:
        show_message("Cảnh báo", "Ngày bắt đầu không thể lớn hơn ngày kết thúc.", "warning")
        # messagebox.showwarning("Cảnh báo", "Ngày bắt đầu không thể lớn hơn ngày kết thúc.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    if employee_id:
        cursor.execute("""
            SELECT Leave.PersonId, People.Name, Leave.Date, Leave.LeaveType, Leave.Reason
            FROM Leave
            JOIN People ON Leave.PersonId = People.Id
            WHERE Leave.Date BETWEEN ? AND ? AND Leave.PersonId = ?
            ORDER BY Leave.Date ASC
        """, (start_date, end_date, employee_id))
    else:
        cursor.execute("""
            SELECT Leave.PersonId, People.Name, Leave.Date, Leave.LeaveType, Leave.Reason
            FROM Leave
            JOIN People ON Leave.PersonId = People.Id
            WHERE Leave.Date BETWEEN ? AND ?
            ORDER BY Leave.Date ASC
        """, (start_date, end_date))

    leaves = cursor.fetchall()
    conn.close()

    for row in tree.get_children():
        tree.delete(row)

    for leave in leaves:
        leave_date = datetime.strptime(leave[2], '%Y-%m-%d')
        formatted_date = leave_date.strftime('%d/%m/%Y')
        tree.insert("", tk.END, values=(leave[0], leave[1], formatted_date, leave[3], leave[4]))

    if not leaves:
        # tk.messagebox.showinfo("Không có dữ liệu", "Không có nhân viên nào nghỉ phép trong khoảng thời gian này.")
        show_message("Không có dữ liệu", "Không có nhân viên nào nghỉ phép trong khoảng thời gian này.", "info")


def edit_leave(tree):
    selected_item = tree.selection()
    if not selected_item:
        show_message("Cảnh báo", "Vui lòng chọn một mục để chỉnh sửa.", "warning")
        # messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mục để chỉnh sửa.")
        return

    item = tree.item(selected_item)
    leave_id = item["values"][0]
    person_id = item["values"][0]
    person_name = item["values"][1]
    leave_date = datetime.strptime(item["values"][2], '%d/%m/%Y')
    leave_type = item["values"][3]
    reason = item["values"][4]

    edit_window = tk.Toplevel()
    edit_window.title("Chỉnh Sửa Nghỉ Phép")
    center_window(edit_window, 600, 300)

    tk.Label(edit_window, text="Mã Nhân Viên:").grid(row=0, column=0, padx=10, pady=5)
    person_id_entry = tk.Entry(edit_window, width=30)
    person_id_entry.insert(0, person_id)
    person_id_entry.grid(row=0, column=1, padx=10, pady=5)
    person_id_entry.config(state="disabled")

    tk.Label(edit_window, text="Tên Nhân Viên:").grid(row=1, column=0, padx=10, pady=5)
    person_name_label = tk.Label(edit_window, text=person_name, width=30, anchor="w", bg="#f0f0f0")
    person_name_label.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Ngày:").grid(row=2, column=0, padx=10, pady=5)
    date_entry = DateEntry(edit_window, date_pattern='dd/mm/yyyy')
    date_entry.set_date(leave_date)
    date_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Loại Nghỉ:").grid(row=3, column=0, padx=10, pady=5)
    leave_type_entry = tk.Entry(edit_window, width=30)
    leave_type_entry.insert(0, leave_type)
    leave_type_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Lý Do:").grid(row=4, column=0, padx=10, pady=5)
    reason_entry = tk.Entry(edit_window, width=30)
    reason_entry.insert(0, reason)
    reason_entry.grid(row=4, column=1, padx=10, pady=5)

    def update_leave_in_db():
        # Lấy thông tin từ form chỉnh sửa
        new_date = date_entry.get_date()  # Ngày chỉnh sửa
        new_type = leave_type_entry.get()  # Loại nghỉ
        new_reason = reason_entry.get()  # Lý do nghỉ

        # Kiểm tra nếu trường Loại Nghỉ hoặc Ngày rỗng
        if not new_type or not new_date:
            show_message("Cảnh báo", "Vui lòng nhập đầy đủ thông tin.", "warning")
            # messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            # Kết nối với cơ sở dữ liệu
            conn = connect_db()
            cursor = conn.cursor()

            # Xử lý old_date để chuyển sang định dạng phù hợp
            old_date = datetime.strptime(item["values"][2], '%d/%m/%Y').strftime('%Y-%m-%d')
            new_date = new_date.strftime('%Y-%m-%d')  # Đảm bảo new_date cũng đúng định dạng
            print(old_date,new_date)
                # Sử dụng ID và ngày cũ để định danh bản ghi cần cập nhật
            cursor.execute("""
                UPDATE Leave
                SET Date = ?, LeaveType = ?, Reason = ?
                WHERE PersonId = ? AND Date = ?
            """, (new_date, new_type, new_reason, leave_id, old_date))

            # Kiểm tra số bản ghi được cập nhật
            if cursor.rowcount > 0:
                conn.commit()
                show_message("Thành công", "Thông tin nghỉ phép đã được cập nhật.", "info")
                # messagebox.showinfo("Thành công", "Thông tin nghỉ phép đã được cập nhật.")
                search_leave_in_range()  # Cập nhật lại danh sách
            else:
                show_message("Không tìm thấy", "Không có dữ liệu để cập nhật.", "warning")
                # messagebox.showwarning("Không tìm thấy", "Không có dữ liệu để cập nhật.")

            conn.close()

        except Exception as e:
            show_message("Lỗi", "Đã xảy ra lỗi khi cập nhật dữ liệu", "error")
            # messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi cập nhật dữ liệu: {e}")

    tk.Button(edit_window, text="Lưu", command=update_leave_in_db, bg="#4CAF50", fg="white").grid(row=5, column=0, columnspan=2, pady=10)


# Cập nhật giao diện chính để thêm nút chỉnh sửa
def view_leaves():
    view_window = tk.Toplevel()
    view_window.title("Xem Thông Tin Nghỉ Phép")
    center_window(view_window, 1000, 600)

    global tree
    tree = ttk.Treeview(view_window, columns=("Mã Nhân Viên", "Tên Nhân Viên", "Ngày", "Loại Nghỉ", "Lý Do"), show='headings')

    tree.heading("Mã Nhân Viên", text="Mã Nhân Viên")
    tree.heading("Tên Nhân Viên", text="Tên Nhân Viên")
    tree.heading("Ngày", text="Ngày")
    tree.heading("Loại Nghỉ", text="Loại Nghỉ")
    tree.heading("Lý Do", text="Lý Do")

    tree.column("Mã Nhân Viên", anchor="center", width=100)
    tree.column("Tên Nhân Viên", anchor="center", width=150)
    tree.column("Ngày", anchor="center", width=100)
    tree.column("Loại Nghỉ", anchor="center", width=100)
    tree.column("Lý Do", anchor="center", width=300)

    search_frame = tk.Frame(view_window)
    search_frame.pack(fill=tk.X, pady=10, padx=10)

    global id_entry, start_date_entry, end_date_entry
    tk.Label(search_frame, text="Mã Nhân Viên:").grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(search_frame, width=15)
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(search_frame, text="Ngày Bắt Đầu:").grid(row=0, column=2, padx=10, pady=5)
    start_date_entry = DateEntry(search_frame, date_pattern='dd/mm/yyyy')
    start_date_entry.grid(row=0, column=3, padx=10, pady=5)

    tk.Label(search_frame, text="Ngày Kết Thúc:").grid(row=0, column=4, padx=10, pady=5)
    end_date_entry = DateEntry(search_frame, date_pattern='dd/mm/yyyy')
    end_date_entry.grid(row=0, column=5, padx=10, pady=5)

    search_button = tk.Button(search_frame, text="Tìm Kiếm", command=search_leave_in_range, bg="#2196F3", fg="white", width=20)
    search_button.grid(row=0, column=6, padx=10)

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    button_frame = tk.Frame(view_window)
    button_frame.pack(pady=10)

    add_button = tk.Button(button_frame, text="Thêm Nghỉ Phép", command=lambda: add_leave_window(view_window), bg="#4CAF50", fg="white", width=15)
    add_button.grid(row=0, column=0, padx=10)

    edit_button = tk.Button(button_frame, text="Chỉnh Sửa", command=lambda: edit_leave(tree), bg="#FF9800", fg="white", width=15)
    edit_button.grid(row=0, column=1, padx=10)

    delete_button = tk.Button(button_frame, text="Xóa", command=lambda: delete_leave(tree), bg="#f44336", fg="white", width=15)
    delete_button.grid(row=0, column=2, padx=10)


def delete_leave(tree):
    selected_item = tree.selection()
    if not selected_item:
        show_message("Cảnh báo", "Vui lòng chọn một mục để xóa.", "warning")
        return

    item = tree.item(selected_item)
    leave_id = item["values"][0]  # Id của mục nghỉ phép
    leave_date = item["values"][2]  # Ngày nghỉ phép
    try:
        # Nếu leave_date là đối tượng DateEntry, ta có thể truy xuất trực tiếp vào ngày
        date = datetime.strptime(leave_date, "%d/%m/%Y").strftime('%Y-%m-%d')
    except Exception as e:
        show_message("Lỗi", f"Định dạng ngày không hợp lệ: {e}", "error")
        return

    print(date)
    # Sử dụng ask_yes_no thay cho messagebox.askyesno
    confirm = ask_yes_no("Xác nhận",
                         f"Bạn có chắc muốn xóa thông tin nghỉ phép với ID: {leave_id} và ngày: {leave_date}?")
    if confirm:
        conn = connect_db()
        cursor = conn.cursor()

        # Xóa thông tin nghỉ phép dựa trên cả Id và Date
        cursor.execute("DELETE FROM Leave WHERE PersonId = ? AND Date = ?", (leave_id, date))
        conn.commit()

        # Kiểm tra xem có xóa được bản ghi không
        if cursor.rowcount > 0:
            tree.delete(selected_item)
            show_message("Thành công", "Thông tin nghỉ phép đã được xóa.", "info")
        else:
            show_message("Thất bại", "Không tìm thấy thông tin nghỉ phép để xóa.", "error")

        conn.close()


def add_leave_window(view_window):
    # Tạo cửa sổ mới để thêm thông tin nghỉ phép
    add_window = tk.Toplevel(view_window)
    add_window.title("Thêm Thông Tin Nghỉ Phép")
    center_window(add_window, 600, 400)  # Căn giữa cửa sổ

    fields = ["Mã Nhân Viên", "Tên Nhân Viên", "Ngày", "Loại Nghỉ", "Lý Do"]
    entries = {}

    # Mã Nhân Viên (Person ID) entry field
    tk.Label(add_window, text="Mã Nhân Viên").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    person_id_entry = tk.Entry(add_window, width=30)
    person_id_entry.grid(row=0, column=1, padx=10, pady=5)

    # Tên Nhân Viên (Employee Name) label - sẽ được cập nhật theo mã nhân viên
    tk.Label(add_window, text="Tên Nhân Viên").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    employee_name_label = tk.Label(add_window, text="")  # Sẽ cập nhật khi người dùng nhập mã nhân viên
    employee_name_label.grid(row=1, column=1, padx=10, pady=5)

    # Cập nhật tên nhân viên theo mã
    def update_employee_name():
        person_id = person_id_entry.get()
        if person_id:
            name = get_employee_name(person_id)
            if name:
                employee_name_label.config(text=name)
            else:
                employee_name_label.config(text="Không tìm thấy nhân viên")
        else:
            employee_name_label.config(text="")

    person_id_entry.bind("<FocusOut>", lambda event: update_employee_name())  # Cập nhật tên khi mất tiêu điểm

    # Lịch để chọn ngày nghỉ
    tk.Label(add_window, text="Ngày").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    leave_date = DateEntry(add_window, date_pattern='dd-mm-yyyy')
    leave_date.grid(row=2, column=1, padx=10, pady=5)

    # Loại Nghỉ (Leave Type) dropdown
    tk.Label(add_window, text="Loại Nghỉ").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    leave_type_combobox = ttk.Combobox(add_window, values=["Paid", "Unpaid"], state="readonly", width=28)
    leave_type_combobox.grid(row=3, column=1, padx=10, pady=5)

    # Lý Do (Reason) nhập liệu
    tk.Label(add_window, text="Lý Do").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    reason_entry = tk.Entry(add_window, width=30)
    reason_entry.grid(row=4, column=1, padx=10, pady=5)

    # Lưu thông tin nghỉ phép
    def save_leave():
        leave_data = {
            "PersonId": person_id_entry.get(),
            "Date": leave_date.get_date(),
            "LeaveType": leave_type_combobox.get(),
            "Reason": reason_entry.get()
        }

        if not leave_data["PersonId"] or not leave_data["Date"] or not leave_data["LeaveType"] or not leave_data[
            "Reason"]:
            show_message("Cảnh báo", "Vui lòng điền đầy đủ thông tin.", "warning")
            # messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin.")
            return

        try:
            person_id = int(leave_data["PersonId"])
        except ValueError:
            show_message("Cảnh báo", "Mã Nhân Viên phải là một số hợp lệ.", "warning")
            # messagebox.showwarning("Cảnh báo", "Mã Nhân Viên phải là một số hợp lệ.")
            return

        # Lưu vào cơ sở dữ liệu
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Leave (PersonId, Date, LeaveType, Reason)
            VALUES (?, ?, ?, ?)
        """, (leave_data["PersonId"], leave_data["Date"], leave_data["LeaveType"], leave_data["Reason"]))
        conn.commit()
        conn.close()
        show_message("Thành công", "Thông tin nghỉ phép đã được lưu.", "info")
        # messagebox.showinfo("Thành công", "Thông tin nghỉ phép đã được lưu.")
        add_window.destroy()  # Đóng cửa sổ thêm

    save_button = tk.Button(add_window, text="Lưu", command=save_leave, bg="#4CAF50", fg="white", width=15)
    save_button.grid(row=5, column=0, columnspan=2, pady=10)