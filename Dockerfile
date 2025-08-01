# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies, including build tools and font tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2-dev \
    pkg-config \
    fonts-noto-cjk \
    fonts-noto-cjk-extra \
    wget \
    unzip \
    fontconfig \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Download and install Pretendard font
RUN wget https://github.com/orioncactus/pretendard/releases/download/v1.3.9/Pretendard-1.3.9.zip -O pretendard.zip && \
    unzip pretendard.zip -d /usr/share/fonts/opentype/pretendard && \
    rm pretendard.zip && \
    fc-cache -fv

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Run app.py when the container launches
CMD ["python", "app.py"] 