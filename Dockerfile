# Use the official Python image from the Docker Hub
FROM python:3.12.4-slim

# Set the working directory in the container
WORKDIR /app

# Install the PostgreSQL client and development libraries
RUN apt-get update \
    && apt-get install -y postgresql-client libpq-dev gcc \
    && apt-get clean

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Specify the command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
