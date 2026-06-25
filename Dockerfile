FROM python:3.10-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (e.g. for scipy, pandas, or postgres connections)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the dependency file and install
COPY pyproject.toml .
# Since we only have pyproject.toml, we can install the current directory package
# Using pip to install from the local directory which contains pyproject.toml
RUN pip install --no-cache-dir build && pip install --no-cache-dir -e .

# Copy the entire project code into the container
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Default command to run the high-performance uvicorn server
CMD ["uvicorn", "scp_core.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
