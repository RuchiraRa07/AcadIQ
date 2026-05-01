from flask import Blueprint, request, jsonify
from models.result import add_result, get_results_by_student, get_all_results, bulk_insert_results
from models.student import get_student_by_id
import csv
import io

results_bp = Blueprint('results', __name__)

@results_bp.route('/results', methods=['POST'])
def create_result():
    data = request.get_json()
    
    required = ['student_id', 'subject', 'marks', 'semester']
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    
    student = get_student_by_id(data['student_id'])
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    if not (0 <= data['marks'] <= data.get('max_marks', 100)):
        return jsonify({"error": "Marks must be between 0 and max_marks"}), 400
    
    result = add_result(
        data['student_id'],
        data['subject'],
        data['marks'],
        data.get('max_marks', 100),
        data['semester']
    )
    
    if result['success']:
        return jsonify({"message": "Result added!"}), 201
    return jsonify({"error": result['error']}), 400

@results_bp.route('/results/student/<int:student_id>', methods=['GET'])
def fetch_student_results(student_id):
    results = get_results_by_student(student_id)
    
    if not results:
        return jsonify({"message": "No results found"}), 404
    return jsonify({"total": len(results), "results": results}), 200

@results_bp.route('/results', methods=['GET'])
def fetch_all_results():
    results = get_all_results()
    return jsonify({"total": len(results), "results": results}), 200

@results_bp.route('/results/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Only CSV files allowed"}), 400
    
    stream = io.StringIO(file.stream.read().decode('utf-8'))
    reader = csv.DictReader(stream)
    
    results_list = []
    errors = []
    
    for i, row in enumerate(reader):
        try:
            student = get_student_by_id(int(row['student_id']))
            if not student:
                errors.append(f"Row {i+1}: Student ID {row['student_id']} not found")
                continue
            
            results_list.append((
                int(row['student_id']),
                row['subject'],
                int(row['marks']),
                int(row.get('max_marks', 100)),
                int(row['semester'])
            ))
        except Exception as e:
            errors.append(f"Row {i+1}: {str(e)}")
    
    if results_list:
        result = bulk_insert_results(results_list)
        return jsonify({
            "message": f"Inserted {result['inserted']} results",
            "errors": errors
        }), 201
    
    return jsonify({"error": "No valid data found", "details": errors}), 400
from models.result import add_result, get_results_by_student, get_all_results, bulk_insert_results, update_result, delete_result

@results_bp.route('/results/<int:result_id>', methods=['PUT'])
def edit_result(result_id):
    data = request.get_json()
    
    if 'marks' not in data:
        return jsonify({"error": "Missing field: marks"}), 400
    
    result = update_result(
        result_id,
        data['marks'],
        data.get('max_marks', 100)
    )
    
    if result['success']:
        return jsonify({"message": "Result updated!"}), 200
    return jsonify({"error": result['error']}), 400

@results_bp.route('/results/<int:result_id>', methods=['DELETE'])
def remove_result(result_id):
    result = delete_result(result_id)
    
    if result['success']:
        return jsonify({"message": "Result deleted!"}), 200
    return jsonify({"error": result['error']}), 404