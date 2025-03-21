# Use official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /project

# Copy all files to the container
COPY . /project

# Upgrade pip before installing anything
RUN python -m pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run Gunicorn with optimized worker count
CMD ["python", "app.py"]

