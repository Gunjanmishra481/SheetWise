from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
from services.validation_service import ValidationService
from utils.file_handler import allowed_file, save_file
import os

# Create a Blueprint for API routes
api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the API is running."""
    return jsonify({"status": "healthy", "service": "TermSheet Validation API"})

@api_bp.route('/validate-term-sheet', methods=['POST'])
@cross_origin()
def validate_term_sheet():
    """
    Endpoint for term sheet validation.
    
    Accepts a file upload (PDF, Word, Excel, image, or text) and returns validation results.
    """
    try:
        print("Received validate-term-sheet request")
        
        # Check if the post request has the file part
        if 'file' not in request.files:
            print("No file part in request")
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        print(f"File received: {file.filename}")
        
        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            print("No selected file")
            return jsonify({'error': 'No selected file'}), 400
        
        # Check if the file is allowed
        try:
            allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'pdf', 'docx', 'xlsx', 'jpg', 'png', 'txt'})
            print(f"Checking if file type is allowed: {file.filename}, allowed extensions: {allowed_extensions}")
            
            if file and allowed_file(file.filename, allowed_extensions):
                # Save the file temporarily
                try:
                    filename = file.filename
                    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
                    print(f"Saving file to {upload_folder}/{filename}")
                    
                    file_path = save_file(file, filename, upload_folder)
                    print(f"File saved to: {file_path}")
                    
                    # Validate the term sheet
                    validation_service = ValidationService()
                    print("Calling validation service")
                    result = validation_service.validate(file_path)
                    print(f"Validation result: {result}")
                    
                    # Clean up the temporary file
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"Removed temporary file: {file_path}")
                    
                    return jsonify(result)
                except Exception as e:
                    print(f"Error processing file: {str(e)}")
                    return jsonify({
                        'status': 'warning',
                        'riskScore': 45,
                        'issues': [
                            {
                                'severity': 'Medium',
                                'description': f'Error processing file: {str(e)}'
                            }
                        ]
                    })
            else:
                print(f"File type not allowed: {file.filename}")
                return jsonify({'error': 'File type not allowed'}), 400
        except Exception as e:
            print(f"Error checking file: {str(e)}")
            return jsonify({
                'status': 'warning',
                'riskScore': 30,
                'issues': [
                    {
                        'severity': 'Low',
                        'description': f'Error checking file: {str(e)}'
                    }
                ]
            })
        
    except Exception as e:
        import traceback
        print(f"Error in validate_term_sheet: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'status': 'warning',
            'riskScore': 50,
            'issues': [
                {
                    'severity': 'High',
                    'description': f'An error occurred during validation: {str(e)}'
                }
            ]
        })

@api_bp.route('/chat', methods=['POST'])
@cross_origin()
def chat():
    """
    Endpoint for chatting with the AI assistant about term sheet analysis.
    
    Request JSON:
    {
        "message": "User's question about the term sheet",
        "termSheetData": { ... term sheet validation results ... }
    }
    
    Response:
    {
        "response": "AI assistant's response to the user's question"
    }
    """
    try:
        # Parse the request data
        data = request.get_json()
        
        if not data or 'message' not in data or 'termSheetData' not in data:
            return jsonify({'error': 'Invalid request. Message and termSheetData are required.'}), 400
        
        user_message = data['message']
        term_sheet_data = data['termSheetData']
        
        # TODO: In a real implementation, you would:
        # 1. Call your AI service (OpenAI, Azure OpenAI, etc.)
        # 2. Pass the user message and term sheet data for context
        # 3. Return the AI's response
        
        # For demo purposes, we'll use a simple rule-based response
        response = generate_demo_response(user_message, term_sheet_data)
        
        return jsonify({'response': response})
    
    except Exception as e:
        current_app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'An error occurred processing your request'}), 500

def generate_demo_response(message, term_sheet_data):
    """Generate a demo response based on the user's message and term sheet data."""
    message_lower = message.lower()
    
    # Check for common question patterns
    if any(word in message_lower for word in ['risk', 'score']):
        score = term_sheet_data.get('riskScore', 0)
        if score < 30:
            return f"The risk score is {score}, which is considered low risk. This term sheet appears to be in good shape."
        elif score < 70:
            return f"The risk score is {score}, which indicates moderate risk. There are some issues that should be addressed."
        else:
            return f"The risk score is {score}, which indicates high risk. This term sheet has significant issues that need to be resolved."
    
    elif any(word in message_lower for word in ['issue', 'problem', 'error']):
        issues = term_sheet_data.get('issues', [])
        if not issues:
            return "No issues were detected in this term sheet."
        
        high_issues = [i for i in issues if i.get('severity', '').lower() == 'high']
        if high_issues:
            return f"I found {len(issues)} issues, including {len(high_issues)} high severity issues. The most critical one is: {high_issues[0].get('description', 'Unknown issue')}"
        else:
            return f"I found {len(issues)} issues, but none are high severity. The most notable one is: {issues[0].get('description', 'Unknown issue')}"
    
    elif any(word in message_lower for word in ['valid', 'status']):
        status = term_sheet_data.get('status', 'unknown')
        if status == 'valid':
            return "This term sheet is valid and ready for processing."
        elif status == 'warning':
            return "This term sheet has some minor issues but is generally valid. You should review the issues before proceeding."
        else:
            return "This term sheet has critical issues that must be resolved before it can be considered valid."
    
    elif any(word in message_lower for word in ['fix', 'resolve', 'solution']):
        return "To resolve the issues, I recommend reviewing each flagged item and updating the term sheet accordingly. Once corrected, you can upload the revised version for another validation check."
    
    elif any(word in message_lower for word in ['summary', 'overview']):
        status = term_sheet_data.get('status', 'unknown')
        score = term_sheet_data.get('riskScore', 0)
        issues = term_sheet_data.get('issues', [])
        
        return f"This term sheet has a validation status of {status} with a risk score of {score}. I detected {len(issues)} issues that need attention. Overall, it {'appears to be in good shape' if score < 30 else 'requires some revisions' if score < 70 else 'needs significant corrections'}."
    
    else:
        return "I'm here to help with your term sheet analysis. You can ask me about the risk score, validation status, specific issues, or how to resolve them. Is there something specific you'd like to know?" 