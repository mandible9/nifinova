# Docker Deployment Guide

This guide explains how to containerize and deploy the Nifty AI Trading Assistant using Docker.

## Quick Start

### 1. Build and Run Locally

```bash
# Build the Docker image
docker build -t nifty-ai-trading .

# Run the container
docker run -p 5000:5000 nifty-ai-trading
```

### 2. Using Docker Compose (Recommended)

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

## Docker Hub Deployment

### 1. Build and Tag for Docker Hub

```bash
# Build the image
docker build -t your-username/nifty-ai-trading:latest .

# Tag with version
docker tag your-username/nifty-ai-trading:latest your-username/nifty-ai-trading:v1.0.0
```

### 2. Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Push latest version
docker push your-username/nifty-ai-trading:latest

# Push tagged version
docker push your-username/nifty-ai-trading:v1.0.0
```

### 3. Pull and Run from Docker Hub

```bash
# Pull the image
docker pull your-username/nifty-ai-trading:latest

# Run the container
docker run -d \
  --name nifty-ai-trading \
  -p 5000:5000 \
  -e ZERODHA_API_KEY="your_api_key" \
  -e ZERODHA_ACCESS_TOKEN="your_access_token" \
  your-username/nifty-ai-trading:latest
```

## Environment Variables

Create a `.env` file for production deployment:

```bash
# API Credentials
ZERODHA_API_KEY=your_zerodha_api_key
ZERODHA_ACCESS_TOKEN=your_zerodha_access_token
WHATSAPP_ACCESS_TOKEN=your_whatsapp_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id

# Application Settings
FLASK_ENV=production
SECRET_KEY=your_secret_key_here
```

## Production Deployment

### Using Docker Compose with Environment File

```bash
# Create .env file with your credentials
cp .env.example .env
# Edit .env with your actual credentials

# Deploy
docker-compose up -d
```

### Health Checks

The container includes health checks that verify the application is running:

```bash
# Check container health
docker ps

# View health check logs
docker inspect --format='{{json .State.Health}}' nifty-ai-trading-app
```

## Scaling and Load Balancing

For production use with multiple instances:

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  nifty-ai-trading:
    image: your-username/nifty-ai-trading:latest
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
    ports:
      - "5000-5002:5000"
```

## Monitoring and Logs

```bash
# View real-time logs
docker-compose logs -f nifty-ai-trading

# View container stats
docker stats nifty-ai-trading-app

# Access container shell
docker exec -it nifty-ai-trading-app /bin/bash
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Use different port
   docker run -p 8080:5000 nifty-ai-trading
   ```

2. **Permission denied**
   ```bash
   # Check file permissions
   ls -la Dockerfile
   chmod +x start_python_server.py
   ```

3. **Build fails**
   ```bash
   # Clean build
   docker build --no-cache -t nifty-ai-trading .
   ```

### Performance Optimization

- Use multi-stage builds for smaller images
- Enable BuildKit for faster builds
- Use specific Python version tags
- Minimize layers in Dockerfile

## Security Considerations

- Never include API keys in the Docker image
- Use environment variables or secrets management
- Run containers as non-root user (already configured)
- Keep base images updated
- Use official Python images only

## Backup and Data Persistence

```bash
# Backup volumes
docker run --rm -v nifty_logs:/backup -v $(pwd):/host alpine tar czf /host/backup.tar.gz /backup

# Restore volumes
docker run --rm -v nifty_logs:/backup -v $(pwd):/host alpine tar xzf /host/backup.tar.gz -C /
```
