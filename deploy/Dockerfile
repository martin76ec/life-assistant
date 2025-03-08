# Base image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y nginx curl && \
    apt-get clean

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH="$HOME/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application code
COPY . /app

# Install dependencies
RUN ~/.local/bin/poetry install

# Configure Nginx
RUN echo 'server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}' > /etc/nginx/conf.d/default.conf

# Start app and Nginx
CMD ["sh", "-c", "nginx && ~/.local/bin/poetry run python app.py"]
