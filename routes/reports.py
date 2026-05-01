from flask import Blueprint, jsonify, send_file
import os
from reports.pdf_report import generate_student_report
from reports.excel_export import generate_excel_report

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports/student/<int:student_id>/pdf', methods=['GET'])
def student_pdf(student_id):
    result = generate_student_report(student_id)
    if 'error' in result:
        return jsonify(result), 404
    return send_file(result['file'], as_attachment=True, download_name=result['filename'])

@reports_bp.route('/reports/excel', methods=['GET'])
def excel_report():
    result = generate_excel_report()
    if 'error' in result:
        return jsonify(result), 500
    return send_file(result['file'], as_attachment=True, download_name=result['filename'])