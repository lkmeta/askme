# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory to the working directory
COPY . .

# Expose the port on which the app runs
EXPOSE 8000

# Set the PYTHONPATH environment variable
ENV PYTHONPATH="/app"

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
