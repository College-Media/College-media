# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to install dependencies
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  
 # Activate virtual environment
RUN python -m venv /app/myenv
ENV PATH="/app/myenv/bin:$PATH"
# Copy the entire project into the container
COPY . .  

# Expose port 8000 for the Django application
EXPOSE 8000  

# Command to run the Django ASGI application using Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "college_media.asgi:application"]
