# Dockerfile
FROM python:3.10-slim

# Updates pip
RUN pip install --upgrade pip

# Install Selenium Python package
RUN pip install selenium

# Set the working directory
WORKDIR /app

# Copy your Python script to the container
COPY ./app /app

# Default command to run the script
# CMD ["python", "/app/selenium_test.py"]