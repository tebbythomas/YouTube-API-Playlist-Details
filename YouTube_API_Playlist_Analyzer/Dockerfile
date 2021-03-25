# Dockerfile

# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#ENV SECRET_KEY="abcdefghi@3325252"
#ENV YOUTUBE_API_KEY="AIzaSyBLLTTMYPMROMDrEbtRX6kZFuWW615GyVQ"

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/