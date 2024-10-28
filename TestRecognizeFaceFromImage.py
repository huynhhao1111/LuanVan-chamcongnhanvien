import face_recognition
import cv2
import pickle
import os

def TestRecognizeFaceFromImage(image_path, tolerance=0.4, display_width=800):
    # Đường dẫn tới tệp encodings
    encodings_path = "encodings/encodings.pickle"

    # Tải dữ liệu encodings
    with open(encodings_path, "rb") as f:
        data = pickle.load(f)

    # Đọc ảnh từ file
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Tìm khuôn mặt trong ảnh và mã hoá chúng
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    # Duyệt qua các khuôn mặt tìm được
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # So khớp khuôn mặt với encodings đã biết
        matches = face_recognition.compare_faces(data["encodings"], face_encoding, tolerance=tolerance)
        name = "Unknown"

        # Nếu tìm thấy ít nhất một khuôn mặt trùng khớp
        if True in matches:
            matched_idxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # Duyệt qua các chỉ số khớp và đếm tần suất tên
            for i in matched_idxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # Lấy tên có số lần xuất hiện nhiều nhất
            name = max(counts, key=counts.get)

        # Vẽ khung chữ nhật quanh khuôn mặt và tên
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 4)
        cv2.putText(image, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.75, (0, 255, 0), 4)

    # Thay đổi kích thước ảnh để hiển thị
    height, width = image.shape[:2]
    aspect_ratio = display_width / float(width)
    display_height = int(height * aspect_ratio)
    resized_image = cv2.resize(image, (display_width, display_height))

    # Hiển thị ảnh với các khuôn mặt nhận diện được
    cv2.imshow("Recognized Faces", resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Đường dẫn tới ảnh cần kiểm tra
    image_path = "Test_Image/test6.jpg"
    TestRecognizeFaceFromImage(image_path)

