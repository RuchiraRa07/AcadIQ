from flask import Flask, send_from_directory
from flask_cors import CORS
from config import SECRET_KEY, DEBUG
from database import init_db
from routes.students import students_bp
from routes.results import results_bp
from routes.analytics import analytics_bp
from routes.predict import predict_bp
from routes.reports import reports_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app)

init_db()

app.register_blueprint(students_bp)
app.register_blueprint(results_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(predict_bp)
app.register_blueprint(reports_bp)

@app.route('/')
def home():
    return {"message": "Student Analytics API is running!"}

@app.route('/dashboard')
def dashboard():
    return send_from_directory('static', 'dashboard.html')

if __name__ == '__main__':
    app.run(debug=DEBUG)