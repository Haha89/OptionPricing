FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the application code to the container
COPY app.py .
COPY dashboard .
COPY option_vol .


# Make port 80 available to the world outside this container
EXPOSE 8050

# Run the command to start uWSGI
CMD ["python", "app.py"]