import pickle
from collections import Counter

# Đọc dữ liệu từ file encodings.pickle
with open("encodings/encodings.pickle", "rb") as f:
    data = pickle.load(f)

names = data.get("names", [])

# Đếm số lượng mã hóa của từng nhân viên
name_counts = Counter(names)

# Hiển thị thông tin
print("Số lượng mã hóa cho từng nhân viên:")
for name, count in name_counts.items():
    print(f"- {name}: {count} mã hóa")

# Tổng quan
print(f"Tổng số mã hóa: {len(data['encodings'])}")
print(f"Tổng số nhân viên: {len(name_counts)}")
