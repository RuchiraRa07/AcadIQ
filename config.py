import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(BASE_DIR, 'data', 'students.db')

SECRET_KEY = 'student_analytics_2026'

DEBUG = True