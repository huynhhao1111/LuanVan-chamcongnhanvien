import os
import tkinter.messagebox as msgbox

def delete_encoding_file():
    encoding_file_path = 'encodings/encodings.pickle'  # Đường dẫn đến file encodings

    # Kiểm tra xem file có tồn tại không
    if os.path.exists(encoding_file_path):
        try:
            os.remove(encoding_file_path)  # Xóa file
            msgbox.showinfo("Thông báo", "Dữ liệu encoding đã được xóa thành công.")
        except Exception as e:
            msgbox.showerror("Lỗi", f"Không thể xóa file: {str(e)}")
    else:
        msgbox.showwarning("Cảnh báo", "File encodings.pickle không tồn tại.")

# Gọi hàm để xóa file encoding
delete_encoding_file()
