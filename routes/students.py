from flask import Blueprint, request, jsonify
from models.student import add_student, get_all_students, get_student_by_id, update_student, delete_student, get_students_by_section, get_sections_summary

students_bp = Blueprint('students', __name__)

@students_bp.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    required = ['name', 'roll_number', 'department', 'semester']
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    result = add_student(
        data['name'], data['roll_number'], data['department'],
        data['semester'], data.get('section', 'A')
    )
    if result['success']:
        return jsonify({"message": "Student added!", "student_id": result['student_id']}), 201
    return jsonify({"error": result['error']}), 400

@students_bp.route('/students', methods=['GET'])
def fetch_all_students():
    students = get_all_students()
    return jsonify({"total": len(students), "students": students}), 200

@students_bp.route('/students/<int:student_id>', methods=['GET'])
def fetch_student(student_id):
    student = get_student_by_id(student_id)
    if student:
        return jsonify(student), 200
    return jsonify({"error": "Student not found"}), 404

@students_bp.route('/students/section/<int:semester>/<section>', methods=['GET'])
def fetch_by_section(semester, section):
    students = get_students_by_section(semester, section)
    return jsonify({"semester": semester, "section": section, "total": len(students), "students": students}), 200

@students_bp.route('/students/sections/summary', methods=['GET'])
def sections_summary():
    summary = get_sections_summary()
    return jsonify({"sections": summary}), 200

@students_bp.route('/students/<int:student_id>', methods=['PUT'])
def edit_student(student_id):
    data = request.get_json()
    required = ['name', 'roll_number', 'department', 'semester']
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    result = update_student(
        student_id, data['name'], data['roll_number'],
        data['department'], data['semester'], data.get('section', 'A')
    )
    if result['success']:
        return jsonify({"message": "Student updated!"}), 200
    return jsonify({"error": result['error']}), 400

@students_bp.route('/students/<int:student_id>', methods=['DELETE'])
def remove_student(student_id):
    result = delete_student(student_id)
    if result['success']:
        return jsonify({"message": "Student deleted!"}), 200
    return jsonify({"error": result['error']}), 404