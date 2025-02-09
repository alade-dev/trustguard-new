# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1




# Install necessary system dependencies for GEOS, gcc, and Python modules
RUN apk add --no-cache \
    python3-dev \
    build-base \
    geos geos-dev \
    musl-dev gcc libffi-dev openssl-dev curl

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose the port the app runs on
EXPOSE 5000

# Health check to ensure service availability
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run the application
CMD ["python", "app.py"]
