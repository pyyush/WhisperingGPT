#!/bin/bash

URL="https://github.com/pyyush/WhisperingGPT.git"
DIR="WhisperingGPT"
IMAGE=$(echo $DIR | tr '[:upper:]' '[:lower:]')

# Install Docker
yum update -y
yum install git docker polkit -y
service docker start
systemctl enable docker

# Clone the Git repository
git clone $URL

# Navigate to the repository directory
cd $DIR

# Build the Docker image
docker build -t $IMAGE .

# Set up OpenAI API Key
OPENAI_API_KEY=

# Start Container
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -d -p 8000:8000 $IMAGE

