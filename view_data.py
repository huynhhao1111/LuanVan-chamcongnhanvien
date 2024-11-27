import sqlite3

# Kết nối đến databaạn
conn = sqlite3.connect('FaceBaseNew.db')
cursor = conn.cursor()

# Truy vấn dữ liệu từ bảng People
cursor.execute("SELECT * FROM AttendanceStatistic")

# Lấy tất cả các hàng dữ liệu
rows = cursor.fetchall()

# In dữ liệu
for row in rows:
    print(row)


# try:
#     cursor.execute("DELETE FROM Attendance WHERE Id = ?", (74,))
#     conn.commit()  # Lưu thay đổi vào database
#     print("Dòng có ID 44 đã được xóa thành công.")
# except sqlite3.Error as e:
#     print(f"Lỗi khi xóa dòng: {e}")


# Đóng kết nối
conn.close()
