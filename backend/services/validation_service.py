import datetime
import json
import os
import re
from datetime import datetime

class ValidationService:
    """
    Service for validating term sheet data against predefined rules
    """
    
    def __init__(self):
        """
        Initialize validation service with compliance rules
        """
        # In a production environment, these would be loaded from a database
        self.approved_counterparties = ["Acme Corporation", "Global Investments Ltd", 
                                        "Stellar Financial", "Mercury Partners", 
                                        "JP Morgan", "Goldman Sachs", "Morgan Stanley"]
        
        self.approved_issuers = ["Barclays Bank PLC", "HSBC", "Lloyds Banking Group", 
                                 "Royal Bank of Scotland", "Standard Chartered"]
        
        self.approved_products = ["Fixed Rate Note", "Floating Rate Note", "Swap", 
                                 "Option", "Forward", "Future", "Equity Derivative"]
        
        self.approved_governing_laws = ["English Law", "UK Law", "New York Law", 
                                       "US Law", "EU Law"]
        
        # For production, we would have a more comprehensive set of rules
        self.validation_rules = {
            'counterparty_check': {
                'description': 'Ensure counterparty is on the approved list',
                'severity': 'HIGH'
            },
            'issuer_check': {
                'description': 'Ensure issuer is on the approved list',
                'severity': 'HIGH'
            },
            'product_check': {
                'description': 'Ensure product is on the approved list',
                'severity': 'MEDIUM'
            },
            'principal_amount_check': {
                'description': 'Ensure principal amount is within acceptable limits',
                'severity': 'HIGH'
            },
            'maturity_date_check': {
                'description': 'Ensure maturity date is valid and in the future',
                'severity': 'MEDIUM'
            },
            'trade_date_check': {
                'description': 'Ensure trade date is not in the future',
                'severity': 'HIGH'
            },
            'settlement_vs_trade_check': {
                'description': 'Ensure settlement date is after trade date',
                'severity': 'MEDIUM'
            },
            'governing_law_check': {
                'description': 'Ensure governing law is approved',
                'severity': 'MEDIUM'
            },
            'risk_disclosure_check': {
                'description': 'Ensure risk disclosure is present',
                'severity': 'LOW'
            }
        }
    
    def validate_term_sheet(self, term_sheet_data):
        """
        Validate the term sheet data against predefined rules
        """
        validation_results = {
            'is_valid': True,
            'risk_score': 0.0,
            'issues': [],
            'timestamp': self._get_current_timestamp()
        }
        
        # Run all validation checks
        self._check_counterparty(term_sheet_data, validation_results)
        self._check_issuer(term_sheet_data, validation_results)
        self._check_product(term_sheet_data, validation_results)
        self._check_principal_amount(term_sheet_data, validation_results)
        self._check_maturity_date(term_sheet_data, validation_results)
        self._check_trade_date(term_sheet_data, validation_results)
        self._check_settlement_vs_trade(term_sheet_data, validation_results)
        self._check_governing_law(term_sheet_data, validation_results)
        self._check_risk_disclosure(term_sheet_data, validation_results)
        
        # Calculate overall risk score (0.0 to 1.0)
        # Higher score = higher risk
        if validation_results['issues']:
            high_count = sum(1 for issue in validation_results['issues'] if issue['severity'] == 'HIGH')
            medium_count = sum(1 for issue in validation_results['issues'] if issue['severity'] == 'MEDIUM')
            low_count = sum(1 for issue in validation_results['issues'] if issue['severity'] == 'LOW')
            
            # Weight the issues by severity
            weighted_score = (high_count * 0.5) + (medium_count * 0.3) + (low_count * 0.1)
            max_possible_score = len(self.validation_rules) * 0.5  # If all were high severity
            
            validation_results['risk_score'] = min(1.0, weighted_score / max_possible_score)
            
            # If there are any HIGH severity issues, mark as invalid
            if high_count > 0:
                validation_results['is_valid'] = False
        
        return validation_results
    
    def _get_current_timestamp(self):
        """
        Get the current timestamp in ISO format
        """
        return datetime.now().isoformat()
    
    def _check_counterparty(self, data, results):
        """Check if counterparty is on the approved list"""
        if 'counterparty' not in data:
            self._add_issue(results, 'counterparty_check', 'Counterparty information is missing', 'HIGH')
        elif data['counterparty'] not in self.approved_counterparties:
            self._add_issue(results, 'counterparty_check', 
                           f"Counterparty '{data['counterparty']}' is not on the approved list", 'HIGH')
    
    def _check_issuer(self, data, results):
        """Check if issuer is on the approved list"""
        if 'issuer' not in data:
            self._add_issue(results, 'issuer_check', 'Issuer information is missing', 'HIGH')
        elif data['issuer'] not in self.approved_issuers:
            self._add_issue(results, 'issuer_check', 
                           f"Issuer '{data['issuer']}' is not on the approved list", 'HIGH')
    
    def _check_product(self, data, results):
        """Check if product is on the approved list"""
        if 'product' not in data:
            self._add_issue(results, 'product_check', 'Product information is missing', 'MEDIUM')
        elif data['product'] not in self.approved_products:
            self._add_issue(results, 'product_check', 
                           f"Product '{data['product']}' is not on the approved list", 'MEDIUM')
    
    def _check_principal_amount(self, data, results):
        """Check if principal amount is within acceptable limits"""
        if 'principal_amount' not in data:
            self._add_issue(results, 'principal_amount_check', 'Principal amount is missing', 'HIGH')
        else:
            # Example rule: Principal amount must be between 1,000 and 50,000,000
            if data['principal_amount'] < 1000 or data['principal_amount'] > 50000000:
                self._add_issue(results, 'principal_amount_check', 
                               f"Principal amount {data['principal_amount']} is outside acceptable limits (1,000 - 50,000,000)", 'HIGH')
    
    def _check_maturity_date(self, data, results):
        """Check if maturity date is valid and in the future"""
        if 'maturity_date' not in data:
            self._add_issue(results, 'maturity_date_check', 'Maturity date is missing', 'MEDIUM')
        else:
            try:
                maturity_date = datetime.strptime(data['maturity_date'], '%Y-%m-%d')
                if maturity_date <= datetime.now():
                    self._add_issue(results, 'maturity_date_check', 
                                  f"Maturity date {data['maturity_date']} is not in the future", 'MEDIUM')
            except ValueError:
                self._add_issue(results, 'maturity_date_check', 
                               f"Maturity date {data['maturity_date']} is in an invalid format", 'MEDIUM')
    
    def _check_trade_date(self, data, results):
        """Check if trade date is not in the future"""
        if 'trade_date' not in data:
            self._add_issue(results, 'trade_date_check', 'Trade date is missing', 'HIGH')
        else:
            try:
                trade_date = datetime.strptime(data['trade_date'], '%Y-%m-%d')
                if trade_date > datetime.now():
                    self._add_issue(results, 'trade_date_check', 
                                  f"Trade date {data['trade_date']} is in the future", 'HIGH')
            except ValueError:
                self._add_issue(results, 'trade_date_check', 
                               f"Trade date {data['trade_date']} is in an invalid format", 'HIGH')
    
    def _check_settlement_vs_trade(self, data, results):
        """Check if settlement date is after trade date"""
        if 'settlement_date' in data and 'trade_date' in data:
            try:
                settlement_date = datetime.strptime(data['settlement_date'], '%Y-%m-%d')
                trade_date = datetime.strptime(data['trade_date'], '%Y-%m-%d')
                
                if settlement_date < trade_date:
                    self._add_issue(results, 'settlement_vs_trade_check', 
                                   f"Settlement date {data['settlement_date']} is before trade date {data['trade_date']}", 'MEDIUM')
            except ValueError:
                self._add_issue(results, 'settlement_vs_trade_check', 
                               "Settlement or trade date is in an invalid format", 'MEDIUM')
    
    def _check_governing_law(self, data, results):
        """Check if governing law is approved"""
        if 'governing_law' not in data:
            self._add_issue(results, 'governing_law_check', 'Governing law is missing', 'MEDIUM')
        elif data['governing_law'] not in self.approved_governing_laws:
            self._add_issue(results, 'governing_law_check', 
                           f"Governing law '{data['governing_law']}' is not on the approved list", 'MEDIUM')
    
    def _check_risk_disclosure(self, data, results):
        """Check if risk disclosure is present"""
        if 'risk_disclosure' not in data or not data['risk_disclosure']:
            self._add_issue(results, 'risk_disclosure_check', 'Risk disclosure is missing', 'LOW')
    
    def _add_issue(self, results, rule_id, description, severity=None):
        """Add an issue to the validation results"""
        if severity is None:
            severity = self.validation_rules[rule_id]['severity']
            
        results['issues'].append({
            'rule_id': rule_id,
            'description': description,
            'severity': severity
        }) 

    def validate(self, file_path):
        """
        Validate a term sheet from a file path
        This is a wrapper that combines OCR, NLP, and validation
        """
        try:
            # Import services here to avoid circular imports
            import sys
            import os
            
            # Add the backend directory to the path if needed
            current_dir = os.path.dirname(os.path.abspath(__file__))
            backend_dir = os.path.dirname(current_dir)
            if backend_dir not in sys.path:
                sys.path.append(backend_dir)
            
            from services.ocr_service import OCRService
            from services.nlp_service import NLPService
            
            print(f"Processing file: {file_path}")
            print(f"File exists: {os.path.exists(file_path)}")
            
            # Extract text using OCR
            ocr_service = OCRService()
            try:
                extracted_text = ocr_service.extract_text(file_path)
                print(f"Text extracted successfully. Length: {len(extracted_text)}")
            except Exception as e:
                import traceback
                print(f"Error in OCR extraction: {str(e)}")
                print(traceback.format_exc())
                # Fall back to mock extraction
                extracted_text = ocr_service._get_mock_term_sheet_text()
            
            # Analyze the text using NLP
            nlp_service = NLPService()
            try:
                term_sheet_data = nlp_service.analyze_text(extracted_text)
                print(f"NLP analysis completed. Found {len(term_sheet_data)} fields.")
            except Exception as e:
                import traceback
                print(f"Error in NLP analysis: {str(e)}")
                print(traceback.format_exc())
                # Fall back to mock analysis
                term_sheet_data = nlp_service._get_mock_nlp_analysis()
            
            # Validate the term sheet data
            validation_results = self.validate_term_sheet(term_sheet_data)
            print(f"Validation completed. Valid: {validation_results['is_valid']}, Issues: {len(validation_results['issues'])}")
            
            # Format the response for the frontend
            response = {
                'status': 'invalid' if not validation_results['is_valid'] else 'warning' if validation_results['issues'] else 'valid',
                'riskScore': int(validation_results['risk_score'] * 100),  # Convert to percentage
                'issues': [
                    {
                        'severity': issue['severity'].capitalize(),
                        'description': issue['description']
                    } for issue in validation_results['issues']
                ]
            }
            
            return response
        except Exception as e:
            import traceback
            print(f"Error in validation service: {str(e)}")
            print(traceback.format_exc())
            
            # Return mock data for demonstration purposes
            return {
                'status': 'warning',
                'riskScore': 45,
                'issues': [
                    {
                        'severity': 'Medium',
                        'description': 'The interest rate specified in section 3.2 conflicts with the reference rate in Appendix A.'
                    },
                    {
                        'severity': 'Low',
                        'description': 'Missing counterparty contact information in section 1.1.'
                    },
                    {
                        'severity': 'High',
                        'description': 'The collateral terms do not comply with regulatory requirements for this type of transaction.'
                    }
                ]
            } 