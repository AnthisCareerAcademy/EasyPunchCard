# Setting up the environment
FROM python:3.10

# Set up the wokring directory. 
WORKDIR /app

# Copies the code to the container
COPY . /app

# Install required pakcages via the requirements.txt file.
RUN pip install --no-cache-dir -r requirements.txt

# Declare a volume for SQLite database file persistence
VOLUME ["/app/database"]

# Run the program. 
CMD ["python", "Clock.py"]
