# Use Python 3.12 Alpine image as base
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Install system dependencies (Alpine uses apk instead of apt-get)
RUN apk add --no-cache \
    build-base \
    curl \
    gcc \
    musl-dev \
    libffi-dev

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip list  # This will show all installed packages for verification

# Verify Python can import the packages
RUN python -c "import fastapi; import openai; import dotenv; import sqlalchemy; import aiosqlite; print('All packages successfully imported!')"

# Copy application code
COPY ./app ./app
COPY ./static ./static

# Create volume for SQLite database
VOLUME ["/app/data"]

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=sqlite:///data/personal_dictionary.db

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 