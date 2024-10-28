import sqlite3

def connect_db():
    """Kết nối đến cơ sở dữ liệu SQLite."""
    conn = sqlite3.connect('FaceBaseNew.db')  # Đặt tên file cơ sở dữ liệu ở đây
    return conn

def get_employees():
    """Lấy tất cả thông tin nhân viên từ cơ sở dữ liệu."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM People")  # Lấy tất cả thông tin nhân viên
    employees = cursor.fetchall()  # Lưu kết quả vào danh sách

    conn.close()  # Đóng kết nối
    return employees
