import sqlite3

def delete_all_people():
    # Kết nối đến cơ sở dữ liệu
    conn = sqlite3.connect('FaceBaseNew.db')
    cursor = conn.cursor()

    # Thực hiện truy vấn xóa tất cả bản ghi
    cursor.execute("DELETE FROM People")

    # Lưu thay đổi và đóng kết nối
    conn.commit()
    conn.close()
    print("Đã xóa tất cả các bản ghi trong bảng People.")

# Gọi hàm để xóa tất cả bản ghi
delete_all_people()
