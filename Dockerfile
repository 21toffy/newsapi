FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install system dependencies with security updates
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        python3-dev \
        musl-dev \
        libpq-dev \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create staticfiles directory
RUN mkdir -p /app/staticfiles

# Skip collectstatic in build - will run at runtime

# Create non-root user with specific UID/GID
RUN groupadd -r appuser --gid=1000 \
    && useradd -r -g appuser --uid=1000 --home-dir=/app --shell=/bin/bash appuser \
    && chown -R appuser:appuser /app \
    && chmod -R 755 /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "newsapi.wsgi:application"]

