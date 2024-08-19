# Use an official Python slim base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /UC_journal_automation

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && apt-get clean

# Install ChromeDriver (for Selenium)
RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    curl -O https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/local/bin/ && \
    rm chromedriver_linux64.zip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

# Copy the application files
COPY . .

# Command to run your Python script
CMD ["python", "main.py"]
