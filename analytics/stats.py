import pandas as pd
import numpy as np
from database import get_connection

def get_all_results_df():
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT r.*, s.name, s.roll_number, s.department, s.semester as student_semester
        FROM results r
        JOIN students s ON r.student_id = s.id
    ''', conn)
    conn.close()
    return df

def calculate_student_stats(student_id):
    df = get_all_results_df()
    student_df = df[df['student_id'] == student_id]
    
    if student_df.empty:
        return None
    
    total_marks = student_df['marks'].sum()
    total_max = student_df['max_marks'].sum()
    percentage = round((total_marks / total_max) * 100, 2)
    
    def get_grade(pct):
        if pct >= 90: return 'O'
        elif pct >= 80: return 'A+'
        elif pct >= 70: return 'A'
        elif pct >= 60: return 'B+'
        elif pct >= 50: return 'B'
        elif pct >= 40: return 'C'
        else: return 'F'
    
    subject_wise = {}
    for _, row in student_df.iterrows():
        pct = round((row['marks'] / row['max_marks']) * 100, 2)
        subject_wise[row['subject']] = {
            "marks": int(row['marks']),
            "max_marks": int(row['max_marks']),
            "percentage": pct,
            "grade": get_grade(pct)
        }
    
    strongest = max(subject_wise, key=lambda x: subject_wise[x]['percentage'])
    weakest = min(subject_wise, key=lambda x: subject_wise[x]['percentage'])
    
    return {
        "student_id": student_id,
        "name": student_df.iloc[0]['name'],
        "roll_number": student_df.iloc[0]['roll_number'],
        "total_marks": int(total_marks),
        "total_max_marks": int(total_max),
        "percentage": percentage,
        "grade": get_grade(percentage),
        "strongest_subject": strongest,
        "weakest_subject": weakest,
        "subject_wise": subject_wise
    }

def calculate_class_stats():
    df = get_all_results_df()
    
    if df.empty:
        return None
    
    student_percentages = []
    for student_id in df['student_id'].unique():
        student_df = df[df['student_id'] == student_id]
        total_marks = student_df['marks'].sum()
        total_max = student_df['max_marks'].sum()
        pct = round((total_marks / total_max) * 100, 2)
        student_percentages.append({
            "student_id": int(student_id),
            "name": student_df.iloc[0]['name'],
            "percentage": pct
        })
    
    pct_series = pd.Series([s['percentage'] for s in student_percentages])
    
    sorted_students = sorted(student_percentages, key=lambda x: x['percentage'], reverse=True)
    for i, s in enumerate(sorted_students):
        s['rank'] = i + 1
        percentile = round(((len(sorted_students) - (i+1)) / len(sorted_students)) * 100, 1)
        s['percentile'] = percentile
    
    subject_averages = {}
    for subject in df['subject'].unique():
        subj_df = df[df['subject'] == subject]
        avg = round((subj_df['marks'].sum() / subj_df['max_marks'].sum()) * 100, 2)
        subject_averages[subject] = avg
    
    pass_count = sum(1 for s in student_percentages if s['percentage'] >= 40)
    
    return {
        "total_students": len(student_percentages),
        "class_average": round(float(pct_series.mean()), 2),
        "highest_score": round(float(pct_series.max()), 2),
        "lowest_score": round(float(pct_series.min()), 2),
        "std_deviation": round(float(pct_series.std()), 2),
        "median": round(float(pct_series.median()), 2),
        "pass_rate": round((pass_count / len(student_percentages)) * 100, 2),
        "subject_averages": subject_averages,
        "leaderboard": sorted_students
    }