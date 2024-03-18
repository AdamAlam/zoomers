# Use a slim Python 3.12 runtime as a base image
FROM python:3.12-slim-bullseye

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./ /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app

# Needed for psycopg2
RUN apt-get update && \
    apt-get install -y libpq-dev gcc 
    
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
