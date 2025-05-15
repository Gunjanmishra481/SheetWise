from flask import Blueprint, request, jsonify, current_app
import os
import uuid
from services.ocr_service import OCRService
from services.nlp_service import NLPService
from services.validation_service import ValidationService
from utils.file_handler import allowed_file, save_file

term_sheet_blueprint = Blueprint('term_sheet', __name__)
ocr_service = OCRService()
nlp_service = NLPService()
validation_service = ValidationService()

@term_sheet_blueprint.route('/validate', methods=['POST'])
def validate_term_sheet():
    """
    Endpoint to validate term sheets uploaded as files
    """
    # Check if file is present in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # If user does not select file, browser might submit an empty file
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
        # Generate a unique filename
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        file_path = save_file(file, filename, current_app.config['UPLOAD_FOLDER'])
        
        # Process the file
        try:
            # Extract text from the file using OCR
            extracted_text = ocr_service.extract_text(file_path)
            
            # Analyze the text using NLP
            nlp_analysis = nlp_service.analyze_text(extracted_text)
            
            # Validate the term sheet
            validation_results = validation_service.validate_term_sheet(nlp_analysis)
            
            return jsonify({
                'status': 'success',
                'filename': file.filename,
                'validation_results': validation_results
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@term_sheet_blueprint.route('/history', methods=['GET'])
def get_validation_history():
    """
    Endpoint to retrieve validation history
    """
    # In a real implementation, this would fetch from a database
    # For now, returning a mock response
    mock_history = [
        {
            'id': '1',
            'filename': 'term_sheet_1.pdf',
            'timestamp': '2023-05-15T10:30:00Z',
            'status': 'VALID',
            'risk_score': 0.2,
            'issues': []
        },
        {
            'id': '2',
            'filename': 'term_sheet_2.pdf',
            'timestamp': '2023-05-14T14:45:00Z',
            'status': 'INVALID',
            'risk_score': 0.8,
            'issues': [
                {'field': 'counterparty', 'severity': 'HIGH', 'description': 'Counterparty not found in approved list'},
                {'field': 'trade_date', 'severity': 'MEDIUM', 'description': 'Trade date is in the past'}
            ]
        }
    ]
    
    return jsonify({'history': mock_history})

@term_sheet_blueprint.route('/chat', methods=['POST'])
def chat_with_agent():
    """
    Endpoint to chat with an AI agent about term sheet analysis
    """
    data = request.json
    
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    
    user_message = data.get('message')
    term_sheet_data = data.get('term_sheet_data', {})
    validation_results = data.get('validation_results', {})
    chat_history = data.get('chat_history', [])
    
    # Generate response based on the user message and context
    response = generate_chat_response(user_message, term_sheet_data, validation_results, chat_history)
    
    return jsonify({
        'response': response,
        'timestamp': validation_service._get_current_timestamp()
    })

def generate_chat_response(message, term_sheet_data, validation_results, chat_history):
    """
    Generate a response for the chat interface
    This is a simple mock implementation - in production, you'd use a proper LLM
    """
    # For the prototype, we'll use simple keyword matching
    message = message.lower()
    
    # Check if there are high severity issues to address
    if validation_results and not validation_results.get('is_valid', True):
        high_severity_issues = [i for i in validation_results.get('issues', []) 
                             if i.get('severity') == 'HIGH']
        if high_severity_issues and 'issue' in message:
            return f"I found {len(high_severity_issues)} high severity issues that need to be addressed. The most critical one is: {high_severity_issues[0].get('description')}"
    
    # Risk assessment response
    if 'risk' in message or 'score' in message:
        risk_score = validation_results.get('risk_score', 0) * 100
        if risk_score < 30:
            return f"The term sheet has a low risk score of {risk_score:.1f}%. It appears to be compliant with our guidelines."
        elif risk_score < 70:
            return f"The term sheet has a moderate risk score of {risk_score:.1f}%. There are some issues that should be reviewed."
        else:
            return f"The term sheet has a high risk score of {risk_score:.1f}%. There are significant compliance issues that must be addressed."
    
    # Information about specific fields
    if 'counterparty' in message:
        counterparty = term_sheet_data.get('counterparty', 'Not specified')
        return f"The counterparty in this term sheet is {counterparty}."
    
    if 'maturity' in message or 'date' in message:
        maturity_date = term_sheet_data.get('maturity_date', 'Not specified')
        return f"The maturity date for this instrument is {maturity_date}."
    
    if 'amount' in message or 'principal' in message:
        currency = term_sheet_data.get('currency', 'USD')
        amount = term_sheet_data.get('principal_amount', 'Not specified')
        if amount != 'Not specified':
            amount_formatted = f"{currency} {amount:,.2f}"
            return f"The principal amount is {amount_formatted}."
        return f"The principal amount is not clearly specified in the term sheet."
    
    # Generic responses for common questions
    if 'hello' in message or 'hi' in message:
        return "Hello! I'm your term sheet analysis assistant. How can I help you with this term sheet?"
    
    if 'thank' in message:
        return "You're welcome! Feel free to ask if you have any other questions about this term sheet."
    
    if 'help' in message:
        return "I can help you understand the term sheet details, explain validation issues, assess risks, and provide guidance on compliance. What would you like to know?"
    
    # Default response
    return "I'm analyzing this term sheet. You can ask me about specific details, risk assessment, or compliance issues, and I'll do my best to help." 