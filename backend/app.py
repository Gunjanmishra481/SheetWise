from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from routes.api_routes import api_bp
from api.term_sheet_api import term_sheet_blueprint
from services.validation_service import ValidationService
from utils.file_handler import allowed_file, save_file

app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'xlsx', 'jpg', 'png', 'txt'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Register blueprints
app.register_blueprint(term_sheet_blueprint, url_prefix='/api/term-sheets')
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "TermSheet Validation API"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2000) 