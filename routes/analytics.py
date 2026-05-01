from flask import Blueprint, jsonify
from analytics.stats import calculate_student_stats, calculate_class_stats
from analytics.trends import get_semester_trends, detect_at_risk_students

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics/student/<int:student_id>', methods=['GET'])
def student_analytics(student_id):
    stats = calculate_student_stats(student_id)
    if not stats:
        return jsonify({"error": "No results found for this student"}), 404
    return jsonify(stats), 200

@analytics_bp.route('/analytics/class', methods=['GET'])
def class_analytics():
    stats = calculate_class_stats()
    if not stats:
        return jsonify({"error": "No results found"}), 404
    return jsonify(stats), 200

@analytics_bp.route('/analytics/trends', methods=['GET'])
def semester_trends():
    trends = get_semester_trends()
    if not trends:
        return jsonify({"error": "No data found"}), 404
    return jsonify(trends), 200

@analytics_bp.route('/analytics/at-risk', methods=['GET'])
def at_risk_students():
    at_risk = detect_at_risk_students()
    return jsonify({
        "total_at_risk": len(at_risk),
        "students": at_risk
    }), 200