#!/bin/bash
set -e

echo "Rebuilding k3s"

kubectl delete namespace alexxapp --ignore-not-found=true
kubectl delete namespace monitoring --ignore-not-found=true

echo "Recreating namespaces..."
kubectl create namespace alexxapp
kubectl create namespace monitoring

echo "Building Docker image and loading into k3s containerd..."

cd xapp

# Build the Docker image
docker build -t alextlittle/nfstream-ml-app:v2 .

echo "Importing image into k3s..."
docker save alextlittle/nfstream-ml-app:v2 | sudo k3s ctr images import -

echo "Deploying app for local development..."
kubectl apply -f ../kubernetes/xapp-dev.yaml -n alexxapp

echo "Setting up monitoring..."
kubectl apply -f ../kubernetes/monitoring.yaml -n monitoring


kubectl wait --for=create pod -l app=prometheus -n monitoring --timeout=30s
kubectl wait --for=create pod -l app=grafana -n monitoring --timeout=30s

echo "Waiting for monitoring pods to be ready..."
kubectl wait --for=condition=ready pod -l app=prometheus -n monitoring --timeout=90s
kubectl wait --for=condition=ready pod -l app=grafana -n monitoring --timeout=90s

echo "Starting port forwarding..."
kubectl port-forward service/prometheus 9090:9090 -n monitoring &
kubectl port-forward service/grafana 3000:3000 -n monitoring &

echo "Done!"
echo "Grafana → http://localhost:3000  (admin/admin)"
echo "Prometheus → http://localhost:9090"

echo "Showing running pods in alexxapp..."
kubectl get pods -n alexxapp
