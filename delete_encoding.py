import pickle
import os
import tkinter.messagebox as msgbox


def delete_encoding_by_id(encoding_file_path, target_id):
    # Kiểm tra xem file encoding có tồn tại không
    if not os.path.exists(encoding_file_path):
        msgbox.showwarning("Cảnh báo", "File encodings.pickle không tồn tại.")
        return

    try:
        # Đọc dữ liệu từ file
        with open(encoding_file_path, "rb") as f:
            data = pickle.load(f)

        # Lấy danh sách encodings và names
        encodings = data.get("encodings", [])
        names = data.get("names", [])

        # Lọc bỏ các mã hóa liên quan đến ID cụ thể
        new_encodings = []
        new_names = []

        for encoding, name in zip(encodings, names):
            # Kiểm tra nếu tên không chứa ID cần xóa, giữ lại
            if not name.endswith(f"_{target_id}"):
                new_encodings.append(encoding)
                new_names.append(name)

        # Ghi lại dữ liệu đã lọc vào file
        with open(encoding_file_path, "wb") as f:
            pickle.dump({"encodings": new_encodings, "names": new_names}, f)

        msgbox.showinfo("Thông báo", "Dữ liệu encoding đã được cập nhật thành công.")
    except Exception as e:
        msgbox.showerror("Lỗi", f"Không thể cập nhật file: {str(e)}")
encoding_file_path = 'encodings/encodings.pickle'
employee_id = "99999"  # ID của nhân viên cần xóa

delete_encoding_by_id(encoding_file_path, employee_id)
