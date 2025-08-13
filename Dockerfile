# Use a specific Python version as the base image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install Python dependencies without storing the cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY . .

# Inform Docker that the container listens on port 5000
EXPOSE 5000

# Set the environment variable to tell Flask where the app is
ENV FLASK_APP=app

# The command to run when the container starts
CMD ["flask", "run", "--host=0.0.0.0"]