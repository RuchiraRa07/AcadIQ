from flask import Blueprint, jsonify
from ml.train import train_models, predict_student

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict/train', methods=['POST'])
def train():
    result = train_models()
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 200

@predict_bp.route('/predict/student/<int:student_id>', methods=['GET'])
def predict(student_id):
    result = predict_student(student_id)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 200