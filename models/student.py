from database import get_connection

def add_student(name, roll_number, department, semester):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO students (name, roll_number, department, semester)
            VALUES (?, ?, ?, ?)
        ''', (name, roll_number, department, semester))
        
        conn.commit()
        student_id = cursor.lastrowid
        conn.close()
        return {"success": True, "student_id": student_id}
    
    except Exception as e:
        conn.close()
        return {"success": False, "error": str(e)}

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    
    return [dict(s) for s in students]

def get_student_by_id(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    student = cursor.fetchone()
    conn.close()
    
    if student:
        return dict(student)
    return None
def update_student(student_id, name, roll_number, department, semester):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE students 
            SET name = ?, roll_number = ?, department = ?, semester = ?
            WHERE id = ?
        ''', (name, roll_number, department, semester, student_id))
        
        conn.commit()
        updated = cursor.rowcount
        conn.close()
        
        if updated == 0:
            return {"success": False, "error": "Student not found"}
        return {"success": True}
    
    except Exception as e:
        conn.close()
        return {"success": False, "error": str(e)}

def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM results WHERE student_id = ?', (student_id,))
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    
    if deleted == 0:
        return {"success": False, "error": "Student not found"}
    return {"success": True}