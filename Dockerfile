# Use a slim Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# 1. Install PyTorch (torch) separately from its official index URL
# This ensures a compatible version is found for your system's architecture (CPU version)
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

# 2. Install the rest of the packages from requirements.txt
# pip will see that torch is already installed and will skip it.
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the Python application
CMD ["python", "app.py"]