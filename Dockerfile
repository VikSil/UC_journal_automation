# Use an official Ubuntu base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /UC_journal_automation

# Copy the application files
COPY . /UC_journal_automation

RUN pip3 install -r requirements.txt

RUN apt-get update && apt-get install -y wget unzip && \
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
apt install -y ./google-chrome-stable_current_amd64.deb && \
rm google-chrome-stable_current_amd64.deb && \
apt-get clean

# Command to run your Python script
CMD ["python3", "main.py"]
