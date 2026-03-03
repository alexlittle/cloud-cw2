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

echo "Setting up monitoring..."
kubectl create namespace monitoring
kubectl apply -f ../kubernetes/monitoring-rbac.yaml
kubectl apply -f ../kubernetes/monitoring-configs.yaml
kubectl apply -f ../kubernetes/monitoring-stack.yaml

echo "Waiting for monitoring stack to be ready..."
kubectl wait --for=condition=ready pod/monitoring-stack -n monitoring --timeout=90s

kubectl create clusterrolebinding minikube-cadvisor \
  --clusterrole=cluster-admin \
  --serviceaccount=monitoring:prometheus-sa

echo "Starting port forwarding..."
kubectl port-forward pod/monitoring-stack 3000:3000 -n monitoring &
kubectl port-forward pod/monitoring-stack 9090:9090 -n monitoring &

echo "Done! Grafana at http://localhost:3000 (admin/admin)"
echo "Prometheus at http://localhost:9090"


# pods running
echo "Showing running pods..."
kubectl get pods -n alexxapp
