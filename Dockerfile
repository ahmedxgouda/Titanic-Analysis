FROM python:3.10-slim

# Set the working directory
WORKDIR /app
# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY app.py .
COPY model_weights.npy .
COPY model_weights_meta.json .
COPY utils.py .

# Expose the port the app runs on
EXPOSE 5000

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]