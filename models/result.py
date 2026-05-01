from database import get_connection

def add_result(student_id, subject, marks, max_marks, semester):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO results (student_id, subject, marks, max_marks, semester)
            VALUES (?, ?, ?, ?, ?)
        ''', (student_id, subject, marks, max_marks, semester))
        
        conn.commit()
        conn.close()
        return {"success": True}
    
    except Exception as e:
        conn.close()
        return {"success": False, "error": str(e)}

def get_results_by_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT r.*, s.name, s.roll_number 
        FROM results r
        JOIN students s ON r.student_id = s.id
        WHERE r.student_id = ?
    ''', (student_id,))
    
    results = cursor.fetchall()
    conn.close()
    return [dict(r) for r in results]

def get_all_results():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT r.*, s.name, s.roll_number, s.department
        FROM results r
        JOIN students s ON r.student_id = s.id
    ''')
    
    results = cursor.fetchall()
    conn.close()
    return [dict(r) for r in results]

def bulk_insert_results(results_list):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.executemany('''
            INSERT INTO results (student_id, subject, marks, max_marks, semester)
            VALUES (?, ?, ?, ?, ?)
        ''', results_list)
        
        conn.commit()
        count = cursor.rowcount
        conn.close()
        return {"success": True, "inserted": count}
    
    except Exception as e:
        conn.close()
        return {"success": False, "error": str(e)}
def update_result(result_id, marks, max_marks):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE results
            SET marks = ?, max_marks = ?
            WHERE id = ?
        ''', (marks, max_marks, result_id))
        
        conn.commit()
        updated = cursor.rowcount
        conn.close()
        
        if updated == 0:
            return {"success": False, "error": "Result not found"}
        return {"success": True}
    
    except Exception as e:
        conn.close()
        return {"success": False, "error": str(e)}

def delete_result(result_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM results WHERE id = ?', (result_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    
    if deleted == 0:
        return {"success": False, "error": "Result not found"}
    return {"success": True}