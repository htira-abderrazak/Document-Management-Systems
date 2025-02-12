# # Use an official Python runtime as a parent image
# FROM python:3.11.6

# # Set environment variables for Python (unbuffered mode) and Django
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set the working directory in the container
# WORKDIR /app

# # Copy the requirements file into the container at /app
# COPY requirements.txt /app/

# # Install any needed packages specified in requirements.txt
# RUN pip install "setuptools<58.0.0"
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the current directory contents into the container at /app
# COPY . /app/

# # Expose port 8000 for the Django application
# EXPOSE 8000

# # Run the Django application with Gunicorn
# CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "DMS.wsgi:application"]

FROM python:3.11.6
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /code
# Install dependencies
# Copy project files
RUN pip install --upgrade pip  

COPY . .
RUN pip install --upgrade pip  

# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Start the application
CMD python manage.py runserver  
