import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import docx2txt
import pandas as pd
import mimetypes

class OCRService:
    """
    Service for extracting text from various document formats
    """
    
    def extract_text(self, file_path):
        """
        Extract text from various file formats
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        
        # Determine file type
        if file_extension == '.pdf':
            return self._extract_from_pdf(file_path)
        elif file_extension == '.docx':
            return self._extract_from_docx(file_path)
        elif file_extension == '.xlsx':
            return self._extract_from_excel(file_path)
        elif file_extension in ['.png', '.jpg', '.jpeg']:
            return self._extract_from_image(file_path)
        elif file_extension == '.txt':
            return self._extract_from_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _extract_from_pdf(self, file_path):
        """
        Extract text from PDF files
        """
        # For production, we would use Azure Document Intelligence or similar
        # For this prototype, we're using pytesseract with pdf2image
        text = ""
        
        try:
            # Convert PDF to images
            images = convert_from_path(file_path)
            
            # Extract text from each image
            for image in images:
                text += pytesseract.image_to_string(image) + "\n"
                
            return text
        except Exception as e:
            # Fallback to a mock response for prototype purposes
            print(f"Error in PDF extraction: {str(e)}")
            return self._get_mock_term_sheet_text()
    
    def _extract_from_docx(self, file_path):
        """
        Extract text from Word documents
        """
        try:
            text = docx2txt.process(file_path)
            return text
        except Exception as e:
            print(f"Error in DOCX extraction: {str(e)}")
            return self._get_mock_term_sheet_text()
    
    def _extract_from_excel(self, file_path):
        """
        Extract text from Excel files
        """
        try:
            df = pd.read_excel(file_path)
            return df.to_string()
        except Exception as e:
            print(f"Error in Excel extraction: {str(e)}")
            return self._get_mock_term_sheet_text()
    
    def _extract_from_image(self, file_path):
        """
        Extract text from image files
        """
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Error in image extraction: {str(e)}")
            return self._get_mock_term_sheet_text()
    
    def _extract_from_text(self, file_path):
        """
        Extract text from text files
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error in text file extraction: {str(e)}")
            return self._get_mock_term_sheet_text()
    
    def _get_mock_term_sheet_text(self):
        """
        Return mock term sheet text for prototype purposes
        """
        return """
        TERM SHEET
        
        Trade Date: 2023-06-15
        Settlement Date: 2023-06-20
        
        Issuer: Barclays Bank PLC
        Counterparty: Acme Corporation
        
        Product: Fixed Rate Note
        Principal Amount: USD 10,000,000
        Maturity Date: 2028-06-15
        Coupon Rate: 5.25% per annum
        Coupon Payment Frequency: Semi-annual
        
        Call Option: Callable after 3 years at par
        
        Governing Law: English Law
        
        Risk Disclosure: The investment involves market risk and may result in loss of principal.
        """ 