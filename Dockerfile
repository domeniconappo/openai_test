FROM python:3.10 as builder

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
RUN poetry install --no-dev

FROM builder as development

# Install additional dependencies required for development and testing
RUN poetry install

# Copy the entire application directory
COPY . /app/

FROM python:3.10-slim as production

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only the necessary files for production
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY src /app/src

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app/src

# Expose the Django development server port (optional, not needed for production)
EXPOSE 8000

# Run the Django development server (optional, not needed for production)
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
