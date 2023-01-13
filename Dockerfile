FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the application code to the container
COPY app.py /app/
COPY ./dashboard /app/dashboard/
COPY ./option_vol /app/option_vol/

# Make port 8050 available to the world outside this container
EXPOSE 8050

# Run the command to start uWSGI
RUN export PYTHONPATH=/app/
CMD ["python", "app.py"]