import sqlite3

def connect_db():
    """Kết nối đến cơ sở dữ liệu SQLite."""
    conn = sqlite3.connect('FaceBaseNew.db')  # Đặt tên file cơ sở dữ liệu ở đây
    return conn

def create_tables():
    """Tạo bảng Attendance và AttendanceStatistic nếu chưa tồn tại."""
    conn = connect_db()
    cursor = conn.cursor()

    # Tạo bảng Attendance
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Attendance (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        PersonId INTEGER,
        Date DATE NOT NULL,
        Time TIME NOT NULL,
        Status TEXT CHECK(Status IN ('In', 'Out')),
        FOREIGN KEY (PersonId) REFERENCES People(id)
    )
    ''')

    # Tạo bảng AttendanceStatistic
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AttendanceStatistic (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        PersonId INTEGER,
        Date DATE NOT NULL,
        TimeIn TIME NOT NULL,
        TimeOut TIME NOT NULL,
        TotalTime INTEGER,
        FOREIGN KEY (PersonId) REFERENCES People(id)
    )
    ''')

    conn.commit()  # Lưu thay đổi
    conn.close()  # Đóng kết nối

if __name__ == "__main__":
    create_tables()  # Tạo bảng nếu chưa tồn tại
