FROM python:3.10-slim as builder

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry and copy only the requirement files
RUN pip install poetry
COPY pyproject.toml poetry.lock /app/

FROM builder as production
# Install production dependencies
RUN poetry install --no-root --no-dev
# Copy the Django project files to the container
COPY . /app/

# Expose the Django development server port
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Stage Dev
FROM builder as development

# Install additional dependencies required for development
RUN poetry install

# Copy the Django project files to the container
COPY . /app/

# Expose the Django development server port
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
