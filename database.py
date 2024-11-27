import sqlite3


def connect_db():
    """Kết nối đến cơ sở dữ liệu SQLite."""
    conn = sqlite3.connect('FaceBaseNew.db')  # Đặt tên file cơ sở dữ liệu ở đây
    return conn


def get_employees():
    """Lấy tất cả thông tin nhân viên từ cơ sở dữ liệu."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM People")  # Lấy tất cả thông tin nhân viên
    employees = cursor.fetchall()  # Lưu kết quả vào danh sách

    conn.close()  # Đóng kết nối
    return employees


def get_leaves(leave_id=None, leave_date=None):
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT Leave.Id, People.Name, Leave.Date, Leave.LeaveType, Leave.Reason FROM Leave JOIN People ON Leave.PersonId = People.Id"

    # Add filters to the query if provided
    conditions = []
    params = []

    if leave_id:
        conditions.append("Leave.Id = ?")
        params.append(leave_id)

    if leave_date:
        conditions.append("Leave.Date = ?")
        params.append(leave_date)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, tuple(params))
    leaves = cursor.fetchall()
    conn.close()

    return leaves


def update_employee(updated_data):
    """Cập nhật thông tin nhân viên dựa trên ID."""
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Cập nhật dữ liệu dựa trên ID
        cursor.execute(
            """
            UPDATE People
            SET Name = ?, Age = ?, Gender = ?, CR = ?, phong_ban = ?
            WHERE ID = ?
            """,
            (updated_data["Tên"], updated_data["Tuổi"], updated_data["Giới tính"], updated_data["Chức vụ"],
             updated_data["Phòng ban"], updated_data["ID"])
        )

        conn.commit()  # Lưu thay đổi
        conn.close()  # Đóng kết nối
        return True
    except Exception as e:
        print("Lỗi khi cập nhật thông tin nhân viên:", e)
        return False

def add_leave(person_id, date, leave_type, reason):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Leave (PersonId, Date, LeaveType, Reason) 
            VALUES (?, ?, ?, ?)
        """, (person_id, date, leave_type, reason))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_column_names():
    """Lấy tên các cột trong bảng People."""
    conn = connect_db()
    cursor = conn.cursor()

    # Lấy thông tin về các cột trong bảng People
    cursor.execute("PRAGMA table_info(People)")
    columns_info = cursor.fetchall()  # Lấy tất cả thông tin cột

    # Đóng kết nối
    conn.close()

    # Lấy tên cột từ thông tin cột
    column_names = [column[1] for column in columns_info]
    return column_names

def get_employee_name(person_id):
    """Fetches the name of an employee based on their PersonId (Mã Nhân Viên)."""
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Query the database to get the name based on PersonId
        cursor.execute("SELECT Name FROM People WHERE Id = ?", (person_id,))
        result = cursor.fetchone()

        if result:
            return result[0]  # Return the name if found
        else:
            return None  # Return None if the PersonId is not found
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()
# In ra tên các cột
print("Tên các cột trong bảng People:", get_column_names())