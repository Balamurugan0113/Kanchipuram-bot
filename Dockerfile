FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files
COPY bot.py .
COPY database.py .

# Expose health check port
EXPOSE 8000

# Run bot
CMD ["python", "bot.py"]
