FROM python:3.9-slim AS backend

WORKDIR /app/backend

# Install system dependencies for OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Create uploads directory
RUN mkdir -p uploads

# Build frontend
FROM node:16-alpine AS frontend-build

WORKDIR /app/frontend

# Copy frontend package.json and install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy frontend code
COPY frontend/ .

# Build frontend
RUN npm run build

# Final image
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy backend from backend stage
COPY --from=backend /app/backend /app/backend
COPY --from=backend /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy built frontend from frontend-build stage
COPY --from=frontend-build /app/frontend/build /app/frontend/build

# Create uploads directory
RUN mkdir -p /app/backend/uploads
RUN chmod 777 /app/backend/uploads

# Set working directory to backend
WORKDIR /app/backend

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"] 