# Use the official Python image as a parent image
FROM python:3.9.19-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . /app

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["python", "main.py"]