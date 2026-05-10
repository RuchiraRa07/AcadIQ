import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score
from ml.train import prepare_data, build_features

def evaluate_models():
    df = prepare_data()
    features_df = build_features(df)
    
    if len(features_df) < 5:
        print("Need at least 5 students to evaluate!")
        return
    
    feature_cols = ['avg_marks', 'std_marks', 'min_marks', 'max_marks_scored', 
                    'subjects_count', 'failed_subjects']
    
    X = features_df[feature_cols]
    y_regression = features_df['overall_percentage']
    y_classifier = features_df['at_risk']
    
    print("=" * 50)
    print("AcadIQ - ML Model Evaluation Report")
    print("=" * 50)
    print(f"Total students in dataset: {len(features_df)}")
    print(f"At-risk students: {y_classifier.sum()}")
    print(f"Safe students: {(y_classifier == 0).sum()}")
    print()

    # ── Regression Evaluation ──────────────────────────
    print("📊 LINEAR REGRESSION (Score Prediction)")
    print("-" * 40)
    
    if len(features_df) >= 10:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_regression, test_size=0.2, random_state=42
        )
        reg = LinearRegression()
        reg.fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"R² Score:              {round(r2, 4)}")
        print(f"Mean Squared Error:    {round(mse, 4)}")
        print(f"Root MSE:              {round(np.sqrt(mse), 4)}")
    
    cv_scores = cross_val_score(LinearRegression(), X, y_regression, cv=3, scoring='r2')
    print(f"Cross-Val R² (3-fold):  {round(cv_scores.mean(), 4)} ± {round(cv_scores.std(), 4)}")
    print()

    # ── Classifier Evaluation ─────────────────────────
    print("🎯 DECISION TREE (At-Risk Classification)")
    print("-" * 40)
    
    if len(features_df) >= 10:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_classifier, test_size=0.2, random_state=42, stratify=y_classifier if y_classifier.sum() >= 2 else None
        )
        clf = DecisionTreeClassifier(max_depth=3, random_state=42)
        clf.fit(X_train, y_train)
        y_pred_clf = clf.predict(X_test)
        
        print(f"Accuracy:  {round(accuracy_score(y_test, y_pred_clf) * 100, 2)}%")
        print()
        print("Classification Report:")
        print(classification_report(y_test, y_pred_clf, 
              target_names=['Safe', 'At-Risk'],
              zero_division=0))
    
    cv_acc = cross_val_score(DecisionTreeClassifier(max_depth=3, random_state=42), 
                              X, y_classifier, cv=3, scoring='accuracy')
    print(f"Cross-Val Accuracy (3-fold): {round(cv_acc.mean() * 100, 2)}% ± {round(cv_acc.std() * 100, 2)}%")

    # ── Feature Importance ────────────────────────────
    print()
    print("🔍 FEATURE IMPORTANCE")
    print("-" * 40)
    clf_full = DecisionTreeClassifier(max_depth=3, random_state=42)
    clf_full.fit(X, y_classifier)
    importances = zip(feature_cols, clf_full.feature_importances_)
    for feature, importance in sorted(importances, key=lambda x: x[1], reverse=True):
        bar = "█" * int(importance * 30)
        print(f"{feature:<25} {bar} {round(importance * 100, 2)}%")

    print()
    print("=" * 50)
    print("Evaluation complete!")
    print("=" * 50)

if __name__ == '__main__':
    evaluate_models()