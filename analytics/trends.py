import pandas as pd
from database import get_connection

def get_semester_trends():
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT r.*, s.name, s.roll_number
        FROM results r
        JOIN students s ON r.student_id = s.id
    ''', conn)
    conn.close()
    
    if df.empty:
        return None
    
    trends = {}
    
    for student_id in df['student_id'].unique():
        student_df = df[df['student_id'] == student_id]
        name = student_df.iloc[0]['name']
        
        semester_data = []
        for sem in sorted(student_df['semester'].unique()):
            sem_df = student_df[student_df['semester'] == sem]
            total = sem_df['marks'].sum()
            total_max = sem_df['max_marks'].sum()
            pct = round((total / total_max) * 100, 2)
            semester_data.append({
                "semester": int(sem),
                "percentage": pct,
                "subjects_count": len(sem_df)
            })
        
        improving = None
        if len(semester_data) > 1:
            first = semester_data[0]['percentage']
            last = semester_data[-1]['percentage']
            improving = last > first
        
        trends[str(student_id)] = {
            "name": name,
            "semester_data": semester_data,
            "improving": improving
        }
    
    return trends

def detect_at_risk_students():
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT r.*, s.name, s.roll_number
        FROM results r
        JOIN students s ON r.student_id = s.id
    ''', conn)
    conn.close()
    
    at_risk = []
    
    for student_id in df['student_id'].unique():
        student_df = df[df['student_id'] == student_id]
        name = student_df.iloc[0]['name']
        roll = student_df.iloc[0]['roll_number']
        
        total = student_df['marks'].sum()
        total_max = student_df['max_marks'].sum()
        overall_pct = round((total / total_max) * 100, 2)
        
        failed_subjects = []
        for _, row in student_df.iterrows():
            pct = (row['marks'] / row['max_marks']) * 100
            if pct < 40:
                failed_subjects.append(row['subject'])
        
        risk_reasons = []
        if overall_pct < 50:
            risk_reasons.append(f"Overall percentage {overall_pct}% is below 50%")
        if len(failed_subjects) > 0:
            risk_reasons.append(f"Failed in: {', '.join(failed_subjects)}")
        if overall_pct < 40:
            risk_reasons.append("At serious risk of not passing")
        
        if risk_reasons:
            at_risk.append({
                "student_id": int(student_id),
                "name": name,
                "roll_number": roll,
                "overall_percentage": overall_pct,
                "risk_reasons": risk_reasons,
                "risk_level": "HIGH" if overall_pct < 40 else "MEDIUM"
            })
    
    return sorted(at_risk, key=lambda x: x['overall_percentage'])