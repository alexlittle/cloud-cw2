#!/bin/bash

echo "rebuilding Minikube setup"
minikube stop
minikube delete

echo "Starting Minikube"
minikube start --cpus 2 --memory 4096 --driver=docker

echo "Create namespaces..."
kubectl create namespace alexxapp
kubectl create namespace monitoring

echo "Setting up Docker env..."
eval $(minikube docker-env)

cd xapp
# Build the Docker image
echo "Building Docker image..."
docker build -t alextlittle/nfstream-ml-app:v2 .

echo "Deploying app ..."
kubectl apply -f ../kubernetes/xapp-dev.yaml -n alexxapp

echo "Set up monitoring..."
kubectl apply -f ../kubernetes/monitoring.yaml

echo "Wait for monitoring "
kubectl wait --for=condition=ready pod -l app=prometheus -n monitoring --timeout=90s
kubectl wait --for=condition=ready pod -l app=grafana -n monitoring --timeout=90s

echo "Starting port forwarding..."
kubectl port-forward service/prometheus 9090:9090 -n monitoring &
kubectl port-forward service/grafana 3000:3000 -n monitoring &

echo "Grafana & Prometheus running"


# pods running
echo "Showing running pods..."
kubectl get pods -n alexxapp
