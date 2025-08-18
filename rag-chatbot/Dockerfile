# Stage 1: Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install poetry
RUN pip install --upgrade pip

# Copy only requirements to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# Stage 2: Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed wheels from builder stage
COPY --from=builder /app/wheels /wheels

# Install dependencies from wheels
RUN pip install --no-cache /wheels/*

# Copy the rest of the application
COPY . .

# Set the python path
ENV PYTHONPATH=/app

# Ingest default data
RUN --mount=type=secret,id=pinecone_api_key --mount=type=secret,id=pinecone_cloud --mount=type=secret,id=pinecone_region python scripts/ingest_data.py

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
