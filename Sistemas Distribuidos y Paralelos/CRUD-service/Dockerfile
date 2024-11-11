# Use a lightweight Python image
FROM python:3.9-slim

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file to the working directory
COPY requirements.txt ./

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app.py to the working directory
COPY app.py ./

# Copy the src folder if it exists
COPY src ./src/  

# Expose the port on which the Flask app runs (default is 5000)
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
