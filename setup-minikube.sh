#!/bin/bash

# Stop and delete Minikube
echo "rebuilding Minikube setup"
minikube stop
minikube delete

# Start minikube
echo "Starting Minikube"
minikube start --cpus 2 --memory 2048 --driver=docker

# Create the nfstream namespace
echo "Creating nfstream namespace..."
kubectl create namespace nfstream

# Set up docker env
echo "Setting up Docker env..."
eval $(minikube docker-env)

# go to docker build dir
cd nfstream
# Build the Docker image
echo "Building Docker image..."
docker build -t alextlittle/nfstream-ml-app:v2 .

echo "Deploying app for local development..."
kubectl apply -f ../kubernetes/nfstream-dev.yaml -n nfstream

# pods running
echo "Showing running pods..."
kubectl get pods -n nfstream
