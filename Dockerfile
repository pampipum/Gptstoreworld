# Use an official lightweight Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies
# Consider using a requirements.txt for managing dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Make a different port available to the world outside this container
# Define PORT as an environment variable or pass it in docker run command for flexibility
EXPOSE 8081

# Run app.py using gunicorn when the container launches
# Update the bind port to 8081 or another port if 8081 is already in use
CMD ["gunicorn", "-w", "4", "-b", ":8081", "--timeout", "130", "main:app"]

