import sqlite3
import random

conn = sqlite3.connect('data/students.db')
cursor = conn.cursor()

cursor.execute("SELECT id, semester FROM students WHERE id > 45")
students = cursor.fetchall()

sem3_subjects = ['Mathematics', 'Physics', 'Chemistry', 'English']
sem4_subjects = ['Data Structures', 'DBMS', 'OS', 'CN']

def get_marks(performance):
    if performance == 'excellent':
        return random.randint(85, 99)
    elif performance == 'good':
        return random.randint(70, 84)
    elif performance == 'average':
        return random.randint(55, 69)
    elif performance == 'poor':
        return random.randint(40, 54)
    else:
        return random.randint(25, 39)

performances = ['excellent', 'good', 'average', 'poor', 'failing']
weights = [0.20, 0.30, 0.25, 0.15, 0.10]

inserted = 0
for student_id, semester in students:
    performance = random.choices(performances, weights=weights)[0]
    subjects = sem3_subjects if semester == 3 else sem4_subjects
    
    for subject in subjects:
        marks = get_marks(performance)
        try:
            cursor.execute('''
                INSERT INTO results (student_id, subject, marks, max_marks, semester)
                VALUES (?, ?, ?, ?, ?)
            ''', (student_id, subject, marks, 100, semester))
            inserted += 1
        except Exception as e:
            print(f"Error for student {student_id}: {e}")

conn.commit()
conn.close()
print(f"Successfully inserted {inserted} results for {len(students)} students!")