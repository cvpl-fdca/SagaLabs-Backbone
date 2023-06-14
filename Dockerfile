# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /

# Copy the the application code
COPY . .
COPY .flaskenv .
# Copy the .env file
COPY .env .

RUN pip install --no-cache-dir -r requirements.txt


# Expose the port on which your Flask app runs
EXPOSE 5000

# Define the command to run your Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
