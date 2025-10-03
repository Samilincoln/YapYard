# Use Python 3.11 slim (safer for Streamlit in production)
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (sqlite3, gcc, curl)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    sqlite3 \
    libsqlite3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Upgrade pip & install dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Healthcheck to ensure Streamlit started
# HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
#   CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Use environment variables for flexibility
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Run the Streamlit app (replace main.py with your actual file if not app.py!)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]








# # Use Python 3.11 slim image for smaller size
# FROM python:3.11-slim

# # Set working directory
# WORKDIR /app

# # Install system dependencies needed for the app
# RUN apt-get update && apt-get install -y \
#     gcc \
#     g++ \
#     build-essential \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# # Copy requirements first for better caching
# COPY requirements.txt .

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the entire application
# COPY . .

# # Create necessary directories for the app
# RUN mkdir -p .crewai_storage

# # Expose the port that Streamlit runs on
# EXPOSE 8501

# # Set environment variables for Railway
# ENV STREAMLIT_SERVER_PORT=8501
# ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
# ENV STREAMLIT_SERVER_HEADLESS=true
# ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
# ENV PYTHONUNBUFFERED=1

# # Health check
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#   CMD curl -f http://localhost:8501/_stcore/health || exit 1

# # Run the Streamlit app
# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.1"]