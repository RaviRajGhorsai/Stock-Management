FROM python:3.12-slim

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install uv and Python dependencies
RUN pip install --upgrade pip \
    && pip install uv \
    && uv sync --frozen --no-dev

# Copy project files
COPY . .

# Make entrypoint executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port
EXPOSE 8800

# Entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["uv", "run", "gunicorn", "Stock.wsgi:application", "--bind", "0.0.0.0:8800"]
