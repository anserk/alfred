# Use an official Python runtime as a parent image
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /app

# Install uv package manager
RUN pip install uv

# Copy the pyproject.toml or other relevant dependency files
COPY pyproject.toml ./

# Install dependencies using uv
RUN uv sync --active

# Copy the rest of the backend application code
COPY . .

# Expose the port the app runs on (8000 is FastAPI's default port)
EXPOSE 8000


CMD ["uv", "run", "fastapi", "dev", "--port", "8000", "--host", "0.0.0.0"]