import re
import json
import os
from datetime import datetime

class NLPService:
    """
    Service for performing NLP analysis on term sheet text
    """
    
    def analyze_text(self, text):
        """
        Analyze the extracted text from term sheets
        In a production environment, this would use Azure OpenAI or similar services
        """
        try:
            # For demonstration purposes, we'll use regex pattern matching
            # In a real implementation, use a proper NLP model like Azure OpenAI
            
            # Extract key information using regex patterns
            term_sheet_data = {}
            
            # Trade and settlement dates
            trade_date_match = re.search(r'Trade Date:\s*(\d{4}-\d{2}-\d{2})', text)
            if trade_date_match:
                term_sheet_data['trade_date'] = trade_date_match.group(1)
            
            settlement_date_match = re.search(r'Settlement Date:\s*(\d{4}-\d{2}-\d{2})', text)
            if settlement_date_match:
                term_sheet_data['settlement_date'] = settlement_date_match.group(1)
            
            # Counterparties
            issuer_match = re.search(r'Issuer:\s*([^\n]+)', text)
            if issuer_match:
                term_sheet_data['issuer'] = issuer_match.group(1).strip()
            
            counterparty_match = re.search(r'Counterparty:\s*([^\n]+)', text)
            if counterparty_match:
                term_sheet_data['counterparty'] = counterparty_match.group(1).strip()
            
            # Product details
            product_match = re.search(r'Product:\s*([^\n]+)', text)
            if product_match:
                term_sheet_data['product'] = product_match.group(1).strip()
            
            principal_match = re.search(r'Principal Amount:\s*([^\n]+)', text)
            if principal_match:
                principal_text = principal_match.group(1).strip()
                # Extract currency and amount
                currency_amount_match = re.search(r'([A-Z]{3})\s*([\d,]+(?:\.\d+)?)', principal_text)
                if currency_amount_match:
                    term_sheet_data['currency'] = currency_amount_match.group(1)
                    # Remove commas and convert to float
                    amount_str = currency_amount_match.group(2).replace(',', '')
                    term_sheet_data['principal_amount'] = float(amount_str)
            
            maturity_date_match = re.search(r'Maturity Date:\s*(\d{4}-\d{2}-\d{2})', text)
            if maturity_date_match:
                term_sheet_data['maturity_date'] = maturity_date_match.group(1)
            
            coupon_rate_match = re.search(r'Coupon Rate:\s*([\d.]+)%', text)
            if coupon_rate_match:
                term_sheet_data['coupon_rate'] = float(coupon_rate_match.group(1))
            
            coupon_frequency_match = re.search(r'Coupon Payment Frequency:\s*([^\n]+)', text)
            if coupon_frequency_match:
                term_sheet_data['coupon_frequency'] = coupon_frequency_match.group(1).strip()
            
            # Legal terms
            governing_law_match = re.search(r'Governing Law:\s*([^\n]+)', text)
            if governing_law_match:
                term_sheet_data['governing_law'] = governing_law_match.group(1).strip()
            
            # Risk disclosure
            risk_disclosure_match = re.search(r'Risk Disclosure:\s*([^\n]+)', text)
            if risk_disclosure_match:
                term_sheet_data['risk_disclosure'] = risk_disclosure_match.group(1).strip()
            
            return term_sheet_data
        except Exception as e:
            print(f"Error in NLP analysis: {str(e)}")
            # Return mock data for prototype purposes
            return self._get_mock_nlp_analysis()
    
    def _get_mock_nlp_analysis(self):
        """
        Return mock NLP analysis for prototype purposes
        """
        return {
            'trade_date': '2023-06-15',
            'settlement_date': '2023-06-20',
            'issuer': 'Barclays Bank PLC',
            'counterparty': 'Acme Corporation',
            'product': 'Fixed Rate Note',
            'currency': 'USD',
            'principal_amount': 10000000.0,
            'maturity_date': '2028-06-15',
            'coupon_rate': 5.25,
            'coupon_frequency': 'Semi-annual',
            'call_option': 'Callable after 3 years at par',
            'governing_law': 'English Law',
            'risk_disclosure': 'The investment involves market risk and may result in loss of principal.'
        } 