# Start from a base image
FROM ubuntu:latest

# Install Python 3.10 and Gunicorn
RUN apt update && \
    apt upgrade -y && \
    apt install -y -q build-essential python3-pip python3-dev && \
    pip3 install fastapi openai gunicorn uvicorn

# Create an application directory
RUN mkdir -p /app

# Copy local assets to the working directory of our docker image
COPY config.py /app/config.py
COPY models.py /app/models.py
COPY main.py /app/main.py

# Set the /app directory as the working directory for any command that follows
WORKDIR /app

# Display Logs on terminal
ENV ACCESS_LOG=/proc/1/fd/1
ENV ERROR_LOG=/proc/1/fd/2

# Expose port 8000
EXPOSE 8000

# Start the server
ENTRYPOINT /usr/local/bin/gunicorn main:app -b 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker --access-logfile "$ACCESS_LOG" --error-logfile "$ERROR_LOG"


