#!/bin/bash
set -e

# make sure minikube isn't running
minikube stop

pkill -f "kubectl port-forward" || true
sleep 2

sudo systemctl start k3s
echo "Rebuilding k3s"

kubectl delete namespace alexxapp --ignore-not-found=true
kubectl delete namespace monitoring --ignore-not-found=true

echo "Recreating namespaces..."
kubectl create namespace alexxapp
kubectl create namespace monitoring

echo "Building Docker image and loading into k3s containerd..."

cd xapp

# Build the Docker image
docker build -t alextlittle/nfstream-ml-app:v3 .

echo "Importing image into k3s..."
docker save alextlittle/nfstream-ml-app:v3 | sudo k3s ctr images import -

echo "Deploying app for local development..."
kubectl apply -f ../kubernetes/xapp-dev.yaml -n alexxapp

echo "Set up monitoring..."
kubectl apply -f ../kubernetes/monitoring.yaml -n monitoring

echo "Wait for pods - needs to be up to port forward & connect to iperf"
kubectl wait --for=condition=ready pod -l app=nfstream -n alexxapp --timeout=120s
kubectl wait --for=create pod -l app=prometheus -n monitoring --timeout=30s
kubectl wait --for=create pod -l app=grafana -n monitoring --timeout=30s

echo "Wait for monitoring pods "
kubectl wait --for=condition=ready pod -l app=prometheus -n monitoring --timeout=90s
kubectl wait --for=condition=ready pod -l app=grafana -n monitoring --timeout=120s
sleep 30

echo "Starting port forwarding..."
kubectl port-forward service/prometheus 9090:9090 -n monitoring &
sleep 2
kubectl port-forward service/grafana 3000:3000 -n monitoring &
sleep 2
kubectl port-forward service/nfstream-service 5201:5201 -n alexxapp &
sleep 2

echo "Showing running pods in alexxapp..."
kubectl get pods -n alexxapp
