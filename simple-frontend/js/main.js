// DOM Elements
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const selectedFileContainer = document.getElementById('selectedFileContainer');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const validateBtn = document.getElementById('validateBtn');
const resultsSection = document.getElementById('resultsSection');
const validationStatus = document.getElementById('validationStatus');
const validationStatusIcon = document.getElementById('validationStatusIcon');
const validationMessage = document.getElementById('validationMessage');
const riskScoreValue = document.getElementById('riskScoreValue');
const scoreBar = document.getElementById('scoreBar');
const issuesList = document.getElementById('issuesList');
const chatSection = document.getElementById('chatSection');
const chatToggleBtn = document.getElementById('chatToggleBtn');
const closeChatBtn = document.getElementById('closeChatBtn');
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendMessageBtn = document.getElementById('sendMessageBtn');
const loadingOverlay = document.getElementById('loadingOverlay');
const loadingMessage = document.getElementById('loadingMessage');

// Global variables
let selectedFile = null;
const API_BASE_URL = 'http://localhost:2000/api';
// For debugging: log the API URL
console.log('Backend API URL:', API_BASE_URL);
let termSheetData = null;
let isBackendAvailable = false;

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    // Hide results and selected file sections initially
    resultsSection.style.display = 'none';
    selectedFileContainer.style.display = 'none';
    chatSection.style.display = 'none';
    loadingOverlay.style.display = 'none';
    
    // Check if backend is available
    checkBackendAvailability();
    
    // Set up event listeners
    setupEventListeners();
    
    // Add welcome message
    showWelcomeMessage();
});

// Check if backend is available
function checkBackendAvailability() {
    console.log('Checking backend availability at:', `${API_BASE_URL}/health`);
    fetch(`${API_BASE_URL}/health`)
        .then(response => {
            if (response.ok) {
                console.log('Backend is available');
                isBackendAvailable = true;
            } else {
                console.error('Backend health check failed with status:', response.status);
                showBackendUnavailableMessage();
            }
        })
        .catch(error => {
            console.error('Backend is unavailable:', error);
            showBackendUnavailableMessage();
        });
}

function showBackendUnavailableMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'backend-unavailable-message';
    messageDiv.innerHTML = `
        <div class="alert">
            <i class="fas fa-exclamation-triangle"></i>
            <p>The backend server appears to be unavailable. You can still explore the interface using mock data.</p>
            <button id="mockDataBtn" class="mock-data-btn">Load Mock Data</button>
        </div>
    `;
    document.querySelector('main').prepend(messageDiv);
    
    document.getElementById('mockDataBtn').addEventListener('click', loadMockData);
}

function showWelcomeMessage() {
    // Create a temporary welcome message
    const welcomeDiv = document.createElement('div');
    welcomeDiv.className = 'welcome-message';
    welcomeDiv.innerHTML = `
        <h2>Welcome to TermSheet Validator!</h2>
        <p>Upload your term sheet document to validate it against our compliance rules.</p>
        <p>Our AI-powered system will analyze your document for issues and provide detailed feedback.</p>
        <div class="welcome-instructions">
            <div class="instruction-step">
                <i class="fas fa-upload"></i>
                <span>Upload your document</span>
            </div>
            <div class="instruction-step">
                <i class="fas fa-check-circle"></i>
                <span>View validation results</span>
            </div>
            <div class="instruction-step">
                <i class="fas fa-comments"></i>
                <span>Chat with our assistant</span>
            </div>
        </div>
    `;
    
    // Insert at the beginning of main
    const mainElement = document.querySelector('main');
    mainElement.insertBefore(welcomeDiv, mainElement.firstChild);
    
    // Fade out and remove after 6 seconds
    setTimeout(() => {
        welcomeDiv.style.opacity = '0';
        setTimeout(() => {
            welcomeDiv.remove();
        }, 1000);
    }, 6000);
}

// Set up all event listeners
function setupEventListeners() {
    // File upload events
    uploadBox.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelection);
    uploadBox.addEventListener('dragover', handleDragOver);
    uploadBox.addEventListener('dragleave', handleDragLeave);
    uploadBox.addEventListener('drop', handleFileDrop);
    
    // Validation button
    validateBtn.addEventListener('click', validateTermSheet);
    
    // Chat controls
    chatToggleBtn.addEventListener('click', toggleChat);
    closeChatBtn.addEventListener('click', toggleChat);
    sendMessageBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', e => {
        if (e.key === 'Enter') sendMessage();
    });
}

// File handling functions
function handleFileSelection(e) {
    const file = e.target.files[0];
    if (file) {
        displaySelectedFile(file);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    uploadBox.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadBox.classList.remove('drag-over');
}

function handleFileDrop(e) {
    e.preventDefault();
    uploadBox.classList.remove('drag-over');
    
    if (e.dataTransfer.files.length) {
        const file = e.dataTransfer.files[0];
        displaySelectedFile(file);
        
        // Also update the file input for consistency
        fileInput.files = e.dataTransfer.files;
    }
}

function displaySelectedFile(file) {
    selectedFile = file;
    
    // Show the selected file container
    selectedFileContainer.style.display = 'flex';
    
    // Update file details
    fileName.textContent = file.name;
    
    // Format file size
    const size = file.size;
    const formattedSize = size < 1024 ? 
        `${size} bytes` : 
        size < 1048576 ? 
        `${(size / 1024).toFixed(2)} KB` : 
        `${(size / 1048576).toFixed(2)} MB`;
    
    fileSize.textContent = formattedSize;
    
    // Set the file icon based on file type
    const fileIcon = document.querySelector('.file-info i');
    const fileType = file.name.split('.').pop().toLowerCase();
    
    switch (fileType) {
        case 'pdf':
            fileIcon.className = 'fas fa-file-pdf';
            break;
        case 'doc':
        case 'docx':
            fileIcon.className = 'fas fa-file-word';
            break;
        case 'xls':
        case 'xlsx':
            fileIcon.className = 'fas fa-file-excel';
            break;
        case 'jpg':
        case 'jpeg':
        case 'png':
            fileIcon.className = 'fas fa-file-image';
            break;
        case 'txt':
            fileIcon.className = 'fas fa-file-alt';
            break;
        default:
            fileIcon.className = 'fas fa-file';
    }
    
    // Scroll to see the validate button
    selectedFileContainer.scrollIntoView({ behavior: 'smooth', block: 'end' });
}

// Term sheet validation
function validateTermSheet() {
    if (!selectedFile) {
        alert('Please select a term sheet file first.');
        return;
    }
    
    console.log('Starting validation for file:', selectedFile.name);
    
    // If backend is unavailable, use mock data
    if (!isBackendAvailable) {
        console.log('Backend unavailable, using mock data');
        loadMockData();
        return;
    }
    
    // Show loading overlay
    loadingOverlay.style.display = 'flex';
    loadingMessage.textContent = 'Analyzing term sheet...';
    
    // Create a FormData object to send the file
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    // Construct the full URL
    const validateUrl = `${API_BASE_URL}/validate-term-sheet`;
    console.log('Sending request to:', validateUrl);
    console.log('FormData content:', selectedFile.name, selectedFile.type, selectedFile.size, 'bytes');
    
    // Make API call to validate the term sheet
    fetch(validateUrl, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log('Response status:', response.status);
        console.log('Response headers:', Object.fromEntries([...response.headers]));
        
        if (!response.ok) {
            throw new Error(`Failed to validate term sheet: ${response.status} ${response.statusText}`);
        }
        
        return response.text().then(text => {
            console.log('Raw response text:', text);
            try {
                return JSON.parse(text);
            } catch (err) {
                console.error('Error parsing JSON:', err);
                throw new Error('Invalid JSON response from server');
            }
        });
    })
    .then(data => {
        console.log('Validation result (parsed):', data);
        if (!data) {
            throw new Error('Empty response from server');
        }
        
        // Store the data
        termSheetData = data;
        
        // Check if data has expected properties
        if (!data.hasOwnProperty('status') || !data.hasOwnProperty('riskScore')) {
            console.warn('Response is missing expected properties:', data);
        }
        
        // Display results
        displayValidationResults(data);
        
        // Hide loading overlay
        loadingOverlay.style.display = 'none';
    })
    .catch(error => {
        console.error('Error during validation:', error);
        
        // Hide loading overlay
        loadingOverlay.style.display = 'none';
        
        // Show error message
        const errorMessage = `An error occurred while validating the term sheet: ${error.message}. Falling back to mock data.`;
        showErrorNotification(errorMessage);
        
        // Fall back to mock data
        setTimeout(() => {
            loadMockData();
        }, 2000);
    });
}

function showErrorNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'error-notification';
    notification.innerHTML = `
        <i class="fas fa-exclamation-circle"></i>
        <span>${message}</span>
        <button><i class="fas fa-times"></i></button>
    `;
    
    // Add to body
    document.body.appendChild(notification);
    
    // Add close button functionality
    notification.querySelector('button').addEventListener('click', () => {
        notification.remove();
    });
    
    // Auto remove after 8 seconds
    setTimeout(() => {
        if (document.body.contains(notification)) {
            notification.classList.add('fade-out');
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    notification.remove();
                }
            }, 500);
        }
    }, 8000);
}

// Display validation results
function displayValidationResults(data) {
    console.log('Displaying validation results:', data);
    
    try {
        // Show results section
        resultsSection.style.display = 'block';
        
        // Update validation status and message
        if (data.status === 'valid') {
            console.log('Status: valid');
            validationStatusIcon.className = 'fas fa-check-circle';
            validationStatusIcon.style.color = '#4caf50';
            validationStatus.textContent = 'Validation Successful';
            validationMessage.textContent = 'This term sheet is valid and ready for processing.';
        } else if (data.status === 'warning') {
            console.log('Status: warning');
            validationStatusIcon.className = 'fas fa-exclamation-triangle';
            validationStatusIcon.style.color = '#ff9800';
            validationStatus.textContent = 'Validation Warning';
            validationMessage.textContent = 'This term sheet has minor issues that should be reviewed.';
        } else {
            console.log('Status: invalid or other:', data.status);
            validationStatusIcon.className = 'fas fa-times-circle';
            validationStatusIcon.style.color = '#f44336';
            validationStatus.textContent = 'Validation Failed';
            validationMessage.textContent = 'This term sheet has critical issues that must be resolved.';
        }
        
        // Update risk score
        const score = data.riskScore || 0;
        console.log('Risk score:', score);
        riskScoreValue.textContent = score;
        scoreBar.style.width = `${score}%`;
        
        // Choose color based on risk score
        if (score < 30) {
            riskScoreValue.style.color = '#4caf50';
        } else if (score < 70) {
            riskScoreValue.style.color = '#ff9800';
        } else {
            riskScoreValue.style.color = '#f44336';
        }
        
        // Display issues
        console.log('Issues:', data.issues);
        displayIssues(data.issues);
        
        // Add initial chat message
        if (chatMessages.children.length === 0) {
            addSystemMessage("I've analyzed your term sheet. What would you like to know about it?");
        }
        
        // Scroll to results section
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
        // Show chat button animation
        animateChatButton();
        
        console.log('Results displayed successfully');
    } catch (error) {
        console.error('Error displaying results:', error);
        showErrorNotification(`Error displaying results: ${error.message}. Using mock data instead.`);
        
        // Fall back to mock data
        setTimeout(() => {
            loadMockData();
        }, 1000);
    }
}

function animateChatButton() {
    chatToggleBtn.classList.add('pulse');
    setTimeout(() => {
        chatToggleBtn.classList.remove('pulse');
    }, 2000);
}

// Display validation issues
function displayIssues(issues) {
    console.log('DisplayIssues called with:', issues);
    
    // Clear the current issues list
    issuesList.innerHTML = '';
    
    if (!issues || issues.length === 0) {
        console.log('No issues to display');
        // No issues found
        issuesList.innerHTML = `
            <div class="no-issues">
                <i class="fas fa-check-circle"></i>
                <p>No issues detected in this term sheet.</p>
            </div>
        `;
        return;
    }
    
    try {
        // Add each issue to the list
        issues.forEach((issue, index) => {
            console.log(`Processing issue ${index}:`, issue);
            
            if (!issue || typeof issue !== 'object') {
                console.warn(`Issue ${index} is not a valid object:`, issue);
                return;
            }
            
            const issueItem = document.createElement('div');
            issueItem.className = 'issue-item';
            
            // Handle case where severity might be missing or invalid
            const severity = issue.severity || 'unknown';
            const severityClass = severity.toLowerCase();
            const severityIcon = getSeverityIcon(severity);
            
            // Handle case where description might be missing
            const description = issue.description || 'Unknown issue';
            
            issueItem.innerHTML = `
                <div class="issue-icon ${severityClass}">
                    <i class="${severityIcon}"></i>
                </div>
                <div class="issue-details">
                    <p>${description}</p>
                    <span class="issue-severity ${severityClass}">${severity}</span>
                </div>
            `;
            
            issuesList.appendChild(issueItem);
        });
    } catch (error) {
        console.error('Error displaying issues:', error);
        
        // Show fallback message
        issuesList.innerHTML = `
            <div class="issue-item">
                <div class="issue-icon medium">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <div class="issue-details">
                    <p>There was an error displaying the issues. Please try again.</p>
                    <span class="issue-severity medium">Error</span>
                </div>
            </div>
        `;
    }
}

// Get the appropriate icon for issue severity
function getSeverityIcon(severity) {
    switch (severity.toLowerCase()) {
        case 'high':
            return 'fas fa-exclamation-circle';
        case 'medium':
            return 'fas fa-exclamation-triangle';
        case 'low':
            return 'fas fa-info-circle';
        default:
            return 'fas fa-circle';
    }
}

// Chat functions
function toggleChat() {
    const isVisible = chatSection.style.display !== 'none';
    chatSection.style.display = isVisible ? 'none' : 'flex';
    
    // If we're opening the chat and there are no messages, add an initial message
    if (!isVisible && chatMessages.children.length === 0 && termSheetData) {
        addSystemMessage("I've analyzed your term sheet. What would you like to know about it?");
    } else if (!isVisible && chatMessages.children.length === 0) {
        addSystemMessage("Welcome! Please validate a term sheet to start the conversation.");
    }
    
    // Focus input when opening
    if (!isVisible) {
        setTimeout(() => messageInput.focus(), 100);
    }
}

function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addUserMessage(message);
    
    // Clear input field
    messageInput.value = '';
    
    // If no term sheet has been validated yet
    if (!termSheetData) {
        addSystemMessage("Please validate a term sheet first so I can help you analyze it.");
        return;
    }
    
    // Show typing indicator
    const typingIndicator = addSystemMessage("Thinking...");
    
    // If backend is unavailable, use mock response
    if (!isBackendAvailable) {
        setTimeout(() => {
            // Remove typing indicator
            chatMessages.removeChild(typingIndicator);
            
            // Add mock response
            generateMockChatResponse(message);
        }, 1500);
        return;
    }
    
    // Send message to API
    fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: message,
            termSheetData: termSheetData
        })
    })
    .then(response => {
        if (!response.ok) throw new Error(`Failed to get response: ${response.status} ${response.statusText}`);
        return response.json();
    })
    .then(data => {
        // Remove typing indicator
        chatMessages.removeChild(typingIndicator);
        
        // Add system response
        addSystemMessage(data.response);
    })
    .catch(error => {
        console.error('Error:', error);
        // Remove typing indicator
        chatMessages.removeChild(typingIndicator);
        addSystemMessage("I'm sorry, I encountered an error. Please try again.");
        
        // Show error notification
        showErrorNotification(`Chat error: ${error.message}. Using mock responses instead.`);
        
        // Use mock response after error
        setTimeout(() => {
            generateMockChatResponse(message);
        }, 2000);
    });
}

function generateMockChatResponse(message) {
    const messageLower = message.toLowerCase();
    let response = "I'm here to help with your term sheet analysis. What would you like to know?";
    
    if (messageLower.includes('risk') || messageLower.includes('score')) {
        response = `The risk score is ${termSheetData.riskScore}, which indicates moderate risk. There are some issues that should be addressed.`;
    } else if (messageLower.includes('issue') || messageLower.includes('problem')) {
        response = "I found 3 issues, including 1 high severity issue. The most critical one is: 'The collateral terms do not comply with regulatory requirements for this type of transaction.'";
    } else if (messageLower.includes('valid')) {
        response = "This term sheet has some minor issues but is generally valid. You should review the issues before proceeding.";
    } else if (messageLower.includes('fix') || messageLower.includes('resolve')) {
        response = "To resolve the issues, I recommend reviewing each flagged item and updating the term sheet accordingly. Once corrected, you can upload the revised version for another validation check.";
    } else if (messageLower.includes('summary') || messageLower.includes('overview')) {
        response = `This term sheet has a validation status of warning with a risk score of ${termSheetData.riskScore}. I detected 3 issues that need attention. Overall, it requires some revisions before it can be approved.`;
    }
    
    addSystemMessage(response);
}

function addUserMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${text}</p>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollChatToBottom();
}

function addSystemMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system';
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${text}</p>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollChatToBottom();
    return messageDiv;
}

function scrollChatToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Mock data for testing
function loadMockData() {
    const mockData = {
        status: 'warning',
        riskScore: 45,
        issues: [
            {
                severity: 'Medium',
                description: 'The interest rate specified in section 3.2 conflicts with the reference rate in Appendix A.'
            },
            {
                severity: 'Low',
                description: 'Missing counterparty contact information in section 1.1.'
            },
            {
                severity: 'High',
                description: 'The collateral terms do not comply with regulatory requirements for this type of transaction.'
            }
        ]
    };
    
    termSheetData = mockData;
    displayValidationResults(mockData);
    
    // If there's a welcome message still showing, remove it
    const welcomeMessage = document.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    // If there's a backend unavailable message, update it
    const backendMessage = document.querySelector('.backend-unavailable-message');
    if (backendMessage) {
        backendMessage.innerHTML = `
            <div class="alert success">
                <i class="fas fa-check-circle"></i>
                <p>Mock data loaded successfully! You can now interact with the interface.</p>
            </div>
        `;
        
        // Remove after 5 seconds
        setTimeout(() => {
            if (document.body.contains(backendMessage)) {
                backendMessage.style.opacity = '0';
                setTimeout(() => {
                    if (document.body.contains(backendMessage)) {
                        backendMessage.remove();
                    }
                }, 500);
            }
        }, 5000);
    }
} 