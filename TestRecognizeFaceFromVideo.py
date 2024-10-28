import face_recognition
import cv2
import pickle
import os


def TestRecognizeFaceFromVideo(video_path, tolerance=0.4, display_width=600, frame_skip=2):
    # Đường dẫn tới tệp encodings
    encodings_path = "encodings/encodings.pickle"

    # Tải dữ liệu encodings
    with open(encodings_path, "rb") as f:
        data = pickle.load(f)

    # Mở video từ đường dẫn
    video_capture = cv2.VideoCapture(video_path)

    # Kiểm tra nếu video không thể mở được
    if not video_capture.isOpened():
        print("Không thể mở video.")
        return

    # Khởi tạo các biến cần thiết
    previous_frame = None
    frame_count = 0

    while True:
        # Đọc từng khung hình của video
        ret, frame = video_capture.read()
        if not ret:
            break  # Nếu không còn khung hình nào để đọc, thoát vòng lặp

        # Giảm tần suất xử lý khung hình
        if frame_count % frame_skip != 0:
            frame_count += 1
            continue

        frame_count += 1

        # Chuyển đổi từ BGR sang RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Chuyển đổi khung hình hiện tại sang màu xám
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Làm mờ khung hình xám để giảm nhiễu
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        # Nếu không có khung hình trước, lưu khung hình hiện tại
        if previous_frame is None:
            previous_frame = gray_frame
            continue

        # Tính toán độ thay đổi giữa hai khung hình
        frame_diff = cv2.absdiff(previous_frame, gray_frame)
        threshold = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]

        # Xóa các khu vực nhỏ không đáng kể
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
        threshold = cv2.dilate(threshold, kernel, iterations=2)

        # Kiểm tra xem có chuyển động hay không
        motion_detected = cv2.countNonZero(threshold) > 50000  # Ngưỡng có thể điều chỉnh

        if motion_detected:
            # Tìm khuôn mặt trong khung hình và mã hoá chúng
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

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
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 4)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.75, (0, 255, 0), 4)

        # Cập nhật khung hình trước
        previous_frame = gray_frame

        # Thay đổi kích thước khung hình để hiển thị
        height, width = frame.shape[:2]
        aspect_ratio = display_width / float(width)
        display_height = int(height * aspect_ratio)
        resized_frame = cv2.resize(frame, (display_width, display_height))

        # Hiển thị khung hình với các khuôn mặt nhận diện được
        cv2.imshow("Recognized Faces from Video", resized_frame)

        # Nhấn 'q' để thoát
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng tài nguyên sau khi hoàn thành
    video_capture.release()
    cv2.destroyAllWindows()
    print("Đã hoàn thành nhận diện từ video.")


if __name__ == "__main__":
    # Đường dẫn tới video cần kiểm tra
    video_path = "Test_Image/video.mp4"  # Thay "path/to/your/video.mp4" bằng đường dẫn video của bạn
    TestRecognizeFaceFromVideo(video_path)
