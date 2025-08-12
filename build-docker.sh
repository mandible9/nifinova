#!/bin/bash

# Build and Deploy Script for Nifty AI Trading Assistant
# Usage: ./build-docker.sh [OPTIONS]

set -e

# Configuration
IMAGE_NAME="nifty-ai-trading"
DOCKER_HUB_USER=${DOCKER_HUB_USER:-"your-username"}
VERSION=${VERSION:-"latest"}
REGISTRY=${REGISTRY:-"docker.io"}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Help function
show_help() {
    cat << EOF
Build and Deploy Script for Nifty AI Trading Assistant

Usage: $0 [OPTIONS]

OPTIONS:
    -h, --help          Show this help message
    -b, --build         Build Docker image only
    -p, --push          Build and push to Docker Hub
    -r, --run           Build and run locally
    -c, --compose       Use docker-compose
    -u, --user USER     Docker Hub username
    -v, --version VER   Image version tag
    --no-cache          Build without cache

Examples:
    $0 --build                          # Build image locally
    $0 --push --user myuser             # Build and push to Docker Hub
    $0 --run                            # Build and run locally
    $0 --compose                        # Use docker-compose
    $0 --push --user myuser --version v1.0.0  # Push with specific version

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -b|--build)
            BUILD_ONLY=true
            shift
            ;;
        -p|--push)
            PUSH_TO_HUB=true
            shift
            ;;
        -r|--run)
            RUN_LOCAL=true
            shift
            ;;
        -c|--compose)
            USE_COMPOSE=true
            shift
            ;;
        -u|--user)
            DOCKER_HUB_USER="$2"
            shift 2
            ;;
        -v|--version)
            VERSION="$2"
            shift 2
            ;;
        --no-cache)
            NO_CACHE="--no-cache"
            shift
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Validate Docker installation
if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed or not in PATH"
    exit 1
fi

# Build image
build_image() {
    log_info "Building Docker image: ${IMAGE_NAME}:${VERSION}"
    
    # Check if Dockerfile exists
    if [[ ! -f "Dockerfile" ]]; then
        log_error "Dockerfile not found in current directory"
        exit 1
    fi
    
    # Build the image
    docker build ${NO_CACHE} -t "${IMAGE_NAME}:${VERSION}" .
    
    if [[ $? -eq 0 ]]; then
        log_success "Image built successfully: ${IMAGE_NAME}:${VERSION}"
    else
        log_error "Failed to build image"
        exit 1
    fi
}

# Push to Docker Hub
push_to_hub() {
    local full_image_name="${DOCKER_HUB_USER}/${IMAGE_NAME}:${VERSION}"
    
    log_info "Tagging image for Docker Hub: ${full_image_name}"
    docker tag "${IMAGE_NAME}:${VERSION}" "${full_image_name}"
    
    log_info "Pushing to Docker Hub: ${full_image_name}"
    docker push "${full_image_name}"
    
    if [[ $? -eq 0 ]]; then
        log_success "Image pushed successfully to Docker Hub"
        log_info "Pull command: docker pull ${full_image_name}"
    else
        log_error "Failed to push image to Docker Hub"
        exit 1
    fi
    
    # Also tag and push as latest if version is not latest
    if [[ "${VERSION}" != "latest" ]]; then
        local latest_image="${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
        log_info "Tagging as latest: ${latest_image}"
        docker tag "${IMAGE_NAME}:${VERSION}" "${latest_image}"
        docker push "${latest_image}"
    fi
}

# Run locally
run_local() {
    log_info "Running container locally on port 5000"
    
    # Stop existing container if running
    if docker ps -q -f name=nifty-ai-trading-local | grep -q .; then
        log_warning "Stopping existing container"
        docker stop nifty-ai-trading-local
        docker rm nifty-ai-trading-local
    fi
    
    # Run new container
    docker run -d \
        --name nifty-ai-trading-local \
        -p 5000:5000 \
        "${IMAGE_NAME}:${VERSION}"
    
    if [[ $? -eq 0 ]]; then
        log_success "Container started successfully"
        log_info "Access the application at: http://localhost:5000"
        log_info "View logs: docker logs -f nifty-ai-trading-local"
        log_info "Stop container: docker stop nifty-ai-trading-local"
    else
        log_error "Failed to start container"
        exit 1
    fi
}

# Use docker-compose
use_compose() {
    if [[ ! -f "docker-compose.yml" ]]; then
        log_error "docker-compose.yml not found"
        exit 1
    fi
    
    log_info "Using docker-compose to build and run"
    docker-compose up --build -d
    
    if [[ $? -eq 0 ]]; then
        log_success "Application started with docker-compose"
        log_info "Access the application at: http://localhost:5000"
        log_info "View logs: docker-compose logs -f"
        log_info "Stop application: docker-compose down"
    else
        log_error "Failed to start with docker-compose"
        exit 1
    fi
}

# Main execution
main() {
    log_info "Starting build process for Nifty AI Trading Assistant"
    
    if [[ "${USE_COMPOSE}" == "true" ]]; then
        use_compose
        exit 0
    fi
    
    # Always build the image first
    build_image
    
    if [[ "${PUSH_TO_HUB}" == "true" ]]; then
        # Check if logged in to Docker Hub
        if ! docker info | grep -q "Username"; then
            log_warning "Not logged in to Docker Hub. Please run: docker login"
            read -p "Continue anyway? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
        push_to_hub
    fi
    
    if [[ "${RUN_LOCAL}" == "true" ]]; then
        run_local
    fi
    
    if [[ "${BUILD_ONLY}" == "true" ]]; then
        log_success "Build completed successfully"
    fi
    
    # Show image info
    log_info "Image details:"
    docker images | grep "${IMAGE_NAME}" | head -5
}

# Run main function
main
