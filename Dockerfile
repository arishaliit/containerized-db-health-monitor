# Use a lightweight Python base image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY monitor.py /app/monitor.py

# Install the PostgreSQL adapter for Python
RUN pip install psycopg2-binary

# Define the default command to run when the container starts.
# This will be overridden by docker-compose, but it's good practice.
CMD ["python", "/app/monitor.py"]