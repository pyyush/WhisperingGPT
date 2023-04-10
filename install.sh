#!/bin/bash

URL="https://github.com/pyyush/WhisperingGPT"
DIR="WhisperingGPT"

# Install Docker & Git
apt-get update
apt-get -y install git-all docker.io
systemctl start docker
systemctl enable docker

# Navigate to home directory
cd ~

# Clone the Git repository
git clone $URL

# Navigate to the repository directory
cd $DIR

# Build the Docker image
docker build -t $DIR .

# Start Container
docker run -p 8000:8000 $DIR


