FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files into the container
COPY app.py .

# Expose the port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port", "8501"]
