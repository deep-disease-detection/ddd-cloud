FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container and install the dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the app files into the container
COPY Home.py Home.py
COPY pages pages
COPY logo.png logo.png
COPY QRcode.png QRcode.png
COPY description.json description.json

# Expose the port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "Home.py", "--server.port", "8501"]
