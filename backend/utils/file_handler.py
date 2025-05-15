import os
import uuid

def allowed_file(filename, allowed_extensions):
    """
    Check if a file has an allowed extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_file(file, filename, upload_folder):
    """
    Save an uploaded file to the specified folder
    """
    # Create the upload folder if it doesn't exist
    os.makedirs(upload_folder, exist_ok=True)
    
    # Create the full path
    file_path = os.path.join(upload_folder, filename)
    
    # Save the file
    file.save(file_path)
    
    return file_path

def generate_unique_filename(original_filename):
    """
    Generate a unique filename based on the original filename
    """
    # Get the file extension
    ext = os.path.splitext(original_filename)[1].lower()
    
    # Generate a unique filename
    unique_name = str(uuid.uuid4()) + ext
    
    return unique_name 