FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (bash + netcat may be needed)
RUN apt-get update && apt-get install -y \
    bash \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy Alembic configuration if needed
COPY alembic.ini /app/alembic.ini

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Expose FastAPI port
EXPOSE 8000

# Use absolute path for entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
