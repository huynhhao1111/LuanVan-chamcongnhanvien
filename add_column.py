import sqlite3

# Kết nối đến cơ sở dữ liệu
conn = sqlite3.connect('FaceBaseNew.db')
cursor = conn.cursor()

# Kiểm tra xem cột 'phong_ban' đã tồn tại chưa
try:
    cursor.execute("ALTER TABLE People ADD COLUMN phong_ban TEXT;")
    print("Đã thêm cột 'phong_ban' vào bảng People.")
except sqlite3.OperationalError as e:
    if "duplicate column name: phong_ban" in str(e):
        print("Cột 'phong_ban' đã tồn tại trong bảng People.")
    else:
        print(f"Lỗi khác: {e}")

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()
