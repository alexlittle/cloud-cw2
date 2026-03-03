#!/bin/bash

# Stop and delete Minikube
echo "rebuilding Minikube setup"
minikube stop
minikube delete

# Start minikube
echo "Starting Minikube"
minikube start --cpus 2 --memory 4096 --driver=docker

# Create the nfstream namespace
echo "Creating nfstream namespace..."
kubectl create namespace alexxapp

# Set up docker env
echo "Setting up Docker env..."
eval $(minikube docker-env)

# go to docker build dir
cd xapp
# Build the Docker image
echo "Building Docker image..."
docker build -t alextlittle/nfstream-ml-app:v2 .

echo "Deploying app for local development..."
kubectl apply -f ../kubernetes/xapp-dev.yaml -n alexxapp

# pods running
echo "Showing running pods..."
kubectl get pods -n alexxapp
