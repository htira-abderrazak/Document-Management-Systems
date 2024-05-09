# Use an official Python runtime as a parent image
FROM python:3.11.6

# Set environment variables for Python (unbuffered mode) and Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install "setuptools<58.0.0"
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose port 80 for the Django development server
EXPOSE 80

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]