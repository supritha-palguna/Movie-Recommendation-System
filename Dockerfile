# Use official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy files
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY tmdb_5000_movies.csv tmdb_5000_movies.csv

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for FastAPI
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
