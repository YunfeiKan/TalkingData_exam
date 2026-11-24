FROM python:3.11-slim

WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js for frontend
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Copy frontend
COPY frontend /app/frontend
WORKDIR /app/frontend
RUN npm install

# Build frontend
RUN npm run build

# Copy backend
WORKDIR /app
COPY backend .

# Create data directory
RUN mkdir -p data

# Expose ports
EXPOSE 5000 3000

# Start both backend and frontend
CMD ["sh", "-c", "python app.py & cd frontend && npm run preview"]
