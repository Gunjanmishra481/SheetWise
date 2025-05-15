import requests
import json

BASE_URL = "http://localhost:2000"

def test_health_check():
    """Test the health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check Status Code:", response.status_code)
    print("Health Check Response:", response.json())
    print()

def test_history_endpoint():
    """Test the validation history endpoint"""
    response = requests.get(f"{BASE_URL}/api/term-sheets/history")
    print("History Status Code:", response.status_code)
    print("History Response:", json.dumps(response.json(), indent=2))
    print()

def test_validation_endpoint(file_path):
    """Test the term sheet validation endpoint"""
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(
            f"{BASE_URL}/api/term-sheets/validate",
            files=files
        )
    print("Validation Status Code:", response.status_code)
    if response.status_code == 200:
        print("Validation Response:", json.dumps(response.json(), indent=2))
    else:
        print("Validation Error:", response.text)
    print()

if __name__ == "__main__":
    # Test health check endpoint
    test_health_check()
    
    # Test history endpoint
    test_history_endpoint()
    
    # Test validation endpoint with a sample PDF file
    # Replace with your actual file path
    test_validation_endpoint("/Users/manash/Downloads/barclaysPrototype/backend/uploads/Term Sheet - INE008A08U84.pdf")