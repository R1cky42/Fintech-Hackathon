# Stage 1: Build React frontend
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
ENV REACT_APP_API_URL=""
RUN npm run build

# Stage 2: Python backend + serve React build
FROM python:3.11-slim
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy React build from stage 1
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Railway sets PORT env var
ENV PORT=5000
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["python", "backend/app.py"]
