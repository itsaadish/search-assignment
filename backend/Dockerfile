# Use official Python image
FROM python:3.11

# Set working directory inside container
WORKDIR /app


# Install system dependencies and Chrome/Chromedriver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy the entire backend code
COPY . .


# Expose Django port
EXPOSE 3100

# # Start Django application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:3100"]
