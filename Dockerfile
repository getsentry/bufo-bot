# Use an official Python runtime as a parent image
FROM python:3.11-alpine
ENV PYTHONUNBUFFERED=True

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip \
    --disable-pip-version-check \
    --no-cache-dir \
    install -r requirements.txt;

# gcloud run deploy --port sets the PORT env var.
EXPOSE $PORT

# Run app.py when the container launches
CMD ["python3", "app.py"]
