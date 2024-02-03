# Setting Python version
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

COPY requirements.txt /tmp

# Install Python packages required to work
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Make port 7373 exposed
EXPOSE 7373

# Copy the MongoDB initialization script into the container
COPY mongodb/init.js /docker-entrypoint-initdb.d/

# Expose MongoDB port if needed (27017 is the default)
EXPOSE 27017

# Run main and garbage_collector_run when the container is launched
CMD ["python", "main.py","garbage_collector_run.py"]
