# SheetWise

**AI-Powered Term Sheet Validation & Compliance Assistant**

SheetWise is an intelligent platform designed to automate and streamline the validation of financial term sheets. Leveraging OCR, NLP, and machine learning, SheetWise helps post-trade teams quickly identify compliance issues, reduce manual effort, and improve accuracy in the term sheet validation process.

---

## Features
- **Drag & Drop Upload:** Easily upload term sheets in PDF, Word, Excel, image, or text formats.
- **AI-Powered Validation:** Automated analysis of key fields and compliance checks using advanced NLP and ML.
- **Risk Scoring:** Instantly see a risk score and validation status for each document.
- **Issue Detection:** Detailed list of detected issues, categorized by severity.
- **Conversational Assistant:** Chat with an AI assistant to ask questions about the analysis and results.
- **Modern UI:** Clean, responsive interface for a seamless user experience.
- **Mock Data Mode:** Explore the interface even if the backend is unavailable.

---

## Getting Started

### Prerequisites
- Python 3.8+
- Flask
- (Optional) Tesseract OCR and Poppler for PDF/image extraction

### Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/YOUR_GITHUB_USERNAME/SheetWise.git
   cd SheetWise
   ```
2. **Install backend dependencies:**
   ```sh
   cd backend
   pip install -r requirements.txt
   ```
3. **Start the backend server:**
   ```sh
   python app.py
   ```
4. **Start the frontend:**
   ```sh
   cd ../simple-frontend
   python -m http.server 3000
   ```
5. **Open your browser:**
   Go to [http://localhost:3000](http://localhost:3000)

---

## Usage
1. Upload a term sheet document.
2. Click **Validate** to analyze the document.
3. Review the validation status, risk score, and detected issues.
4. Use the chat assistant to ask questions or get clarifications.

---

## Project Structure
```
SheetWise/
├── backend/           # Flask backend for validation and OCR/NLP
├── simple-frontend/   # Modern HTML/CSS/JS frontend
└── README.md          # Project documentation
```

---

## Contributing
Contributions are welcome! Please open issues or submit pull requests to help improve SheetWise.

---

## License
This project is licensed under the MIT License.

---

**SheetWise** — Making term sheet validation smarter, faster, and more reliable. 