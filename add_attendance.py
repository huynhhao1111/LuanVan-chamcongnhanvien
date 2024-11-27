import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import sqlite3
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

def add_attendance_form():
    add_window = tk.Toplevel()
    add_window.title("Thêm Chấm Công")

    # Set window size and center on the screen
    window_width = 400
    window_height = 350
    screen_width = add_window.winfo_screenwidth()
    screen_height = add_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)
    add_window.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

    # Set font and colors
    label_font = ('Arial', 12)
    entry_font = ('Arial', 10)
    button_font = ('Arial', 12, 'bold')

    # Create main frame for alignment
    frame = tk.Frame(add_window)
    frame.pack(expand=True)

    # Employee ID input
    tk.Label(frame, text="ID Nhân Viên:", font=label_font).grid(row=0, column=0, pady=10, sticky="e", padx=10)
    id_entry = tk.Entry(frame, font=entry_font)
    id_entry.grid(row=0, column=1, pady=10, padx=10)

    # Display employee name after entering ID
    tk.Label(frame, text="Tên Nhân Viên:", font=label_font).grid(row=1, column=0, pady=10, sticky="e", padx=10)
    name_value = tk.Label(frame, text="", font=entry_font)
    name_value.grid(row=1, column=1, pady=10, padx=10)

    # Function to fetch employee name from ID
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
                    name_value.config(text=name[0])  # Display employee name
                else:
                    name_value.config(text="Không tìm thấy")
            except sqlite3.Error as e:
                show_message("Lỗi", "Lỗi khi tìm kiếm tên nhân viên.", "error")

    # Call function to fetch employee name when ID is entered
    id_entry.bind("<FocusOut>", lambda event: fetch_employee_name())

    # Date input
    tk.Label(frame, text="Ngày:", font=label_font).grid(row=2, column=0, pady=10, sticky="e", padx=10)
    date_entry = DateEntry(frame, date_pattern='dd-mm-yyyy', font=entry_font)
    date_entry.grid(row=2, column=1, pady=10, padx=10)

    # Time In selection
    tk.Label(frame, text="Thời gian vào:", font=label_font).grid(row=3, column=0, pady=10, sticky="e", padx=10)
    time_in_hour = ttk.Combobox(frame, values=[f"{i:02d}" for i in range(24)], width=3, font=entry_font)
    time_in_hour.grid(row=3, column=1, padx=5)
    time_in_minute = ttk.Combobox(frame, values=[f"{i:02d}" for i in range(0, 60, 5)], width=3, font=entry_font)
    time_in_minute.grid(row=3, column=2)
    time_in_hour.set("00")
    time_in_minute.set("00")

    # Time Out selection
    tk.Label(frame, text="Thời gian ra:", font=label_font).grid(row=4, column=0, pady=10, sticky="e", padx=10)
    time_out_hour = ttk.Combobox(frame, values=[f"{i:02d}" for i in range(24)], width=3, font=entry_font)
    time_out_hour.grid(row=4, column=1, padx=5)
    time_out_minute = ttk.Combobox(frame, values=[f"{i:02d}" for i in range(0, 60)], width=3, font=entry_font)
    time_out_minute.grid(row=4, column=2)
    time_out_hour.set("00")
    time_out_minute.set("00")

    # Function to save attendance information
    def save_attendance():
        person_id = id_entry.get()
        name = name_value.cget("text")
        date = date_entry.get_date().strftime('%d-%m-%Y')
        time_in = f"{time_in_hour.get()}:{time_in_minute.get()}:00"
        time_out = f"{time_out_hour.get()}:{time_out_minute.get()}:00"

        if not person_id or not date or not time_in or not time_out:
            show_message("Cảnh báo", "Vui lòng điền đầy đủ thông tin.", "warning")
            return

        try:
            conn = sqlite3.connect('FaceBaseNew.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO AttendanceStatistic (PersonId, Date, TimeIn, TimeOut, TotalTime) VALUES (?, ?, ?, ?, ?)",
                (person_id, date, time_in, time_out, 0))  # TotalTime will be calculated later
            cursor.execute(
                "INSERT INTO Attendance (PersonId, Date, Time, Status) VALUES (?, ?, ?, ?)",
                (person_id, date, time_in, 'In')
            )

            if time_out != "00:00:00":
                cursor.execute(
                    "INSERT INTO Attendance (PersonId, Date, Time, Status) VALUES (?, ?, ?, ?)",
                    (person_id, date, time_out, 'Out')
                )
            conn.commit()
            conn.close()
            show_message("Thông báo", "Thêm chấm công thành công.", "info")

            add_window.destroy()
        except sqlite3.Error as e:
            show_message("Lỗi", "Lỗi khi thêm dữ liệu.", "error")

    # Save button with green color and rounded corners
    save_button = tk.Button(
        frame, text="Lưu", command=save_attendance, font=button_font, bg="#28a745", fg="white", relief="solid", width=12
    )
    save_button.grid(row=5, column=0, columnspan=3, pady=20)

    # Apply custom styling for the button
    save_button.config(
        relief="flat", bd=2, padx=20, pady=10, font=("Arial", 12, "bold"), bg="#28a745", fg="white", activebackground="#218838"
    )
