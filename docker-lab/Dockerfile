# ── Stage 1: Base image ──────────────────────────────────────────────────────
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency list first (leverages Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
