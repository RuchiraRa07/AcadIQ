import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os
from database import get_connection

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

def prepare_data():
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT r.student_id, r.subject, r.marks, r.max_marks, r.semester,
               s.name, s.department
        FROM results r
        JOIN students s ON r.student_id = s.id
    ''', conn)
    conn.close()
    return df

def build_features(df):
    student_features = []
    
    for student_id in df['student_id'].unique():
        student_df = df[df['student_id'] == student_id]
        
        total = student_df['marks'].sum()
        total_max = student_df['max_marks'].sum()
        overall_pct = round((total / total_max) * 100, 2)
        
        avg_marks = round(student_df['marks'].mean(), 2)
        std_marks = round(student_df['marks'].std(), 2) if len(student_df) > 1 else 0
        min_marks = int(student_df['marks'].min())
        max_marks_scored = int(student_df['marks'].max())
        subjects_count = len(student_df)
        failed_subjects = int((student_df['marks'] / student_df['max_marks'] * 100 < 40).sum())
        
        at_risk = 1 if overall_pct < 50 or failed_subjects > 0 else 0
        
        student_features.append({
            "student_id": student_id,
            "overall_percentage": overall_pct,
            "avg_marks": avg_marks,
            "std_marks": std_marks,
            "min_marks": min_marks,
            "max_marks_scored": max_marks_scored,
            "subjects_count": subjects_count,
            "failed_subjects": failed_subjects,
            "at_risk": at_risk
        })
    
    return pd.DataFrame(student_features)

def train_models():
    df = prepare_data()
    features_df = build_features(df)
    
    if len(features_df) < 3:
        return {"error": "Need at least 3 students to train"}
    
    feature_cols = ['avg_marks', 'std_marks', 'min_marks', 'max_marks_scored', 
                    'subjects_count', 'failed_subjects']
    
    X = features_df[feature_cols]
    y_regression = features_df['overall_percentage']
    y_classifier = features_df['at_risk']
    
    regressor = LinearRegression()
    regressor.fit(X, y_regression)
    
    classifier = DecisionTreeClassifier(max_depth=3, random_state=42)
    classifier.fit(X, y_classifier)
    
    train_predictions = classifier.predict(X)
    accuracy = round(accuracy_score(y_classifier, train_predictions) * 100, 2)
    
    models = {
        "regressor": regressor,
        "classifier": classifier,
        "feature_cols": feature_cols,
        "accuracy": accuracy
    }
    
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(models, f)
    
    return {
        "message": "Models trained successfully!",
        "students_trained_on": len(features_df),
        "classifier_accuracy": f"{accuracy}%",
        "feature_cols": feature_cols
    }

def predict_student(student_id):
    if not os.path.exists(MODEL_PATH):
        return {"error": "Model not trained yet. Call /predict/train first"}
    
    df = prepare_data()
    features_df = build_features(df)
    
    student_row = features_df[features_df['student_id'] == student_id]
    if student_row.empty:
        return {"error": "Student not found"}
    
    with open(MODEL_PATH, 'rb') as f:
        models = pickle.load(f)
    
    feature_cols = models['feature_cols']
    X = student_row[feature_cols]
    
    predicted_pct = round(float(models['regressor'].predict(X)[0]), 2)
    at_risk_pred = int(models['classifier'].predict(X)[0])
    at_risk_proba = models['classifier'].predict_proba(X)[0]
    risk_probability = round(float(max(at_risk_proba)) * 100, 2)
    
    return {
        "student_id": student_id,
        "predicted_percentage": predicted_pct,
        "at_risk": bool(at_risk_pred),
        "risk_probability": f"{risk_probability}%",
        "risk_label": "HIGH RISK" if at_risk_pred == 1 else "LOW RISK",
        "recommendation": "Needs immediate attention" if at_risk_pred == 1 else "Performing well"
    }