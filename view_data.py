import sqlite3

# Kết nối đến databaạn
conn = sqlite3.connect('FaceBaseNew.db')
cursor = conn.cursor()

# Truy vấn dữ liệu từ bảng People
cursor.execute("SELECT * FROM People")

# Lấy tất cả các hàng dữ liệu
rows = cursor.fetchall()

# In dữ liệu
for row in rows:
    print(row)

# Đóng kết nối
conn.close()
