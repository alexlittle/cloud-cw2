#!/bin/bash

# stop k3s if running
sudo systemctl stop k3s

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
docker build -t alextlittle/nfstream-ml-app:v3 .

echo "Deploying app ..."
kubectl apply -f ../kubernetes/xapp-dev.yaml

echo "waiting for service to be ready"
until kubectl get svc nfstream-service -n alexxapp >/dev/null 2>&1; do
    printf "."
    sleep 2
done

echo "Set up monitoring..."
kubectl apply -f ../kubernetes/monitoring.yaml

echo "Wait for pods - needs to be up to port forward & connect to iperf"
kubectl wait --for=condition=ready pod -l app=nfstream -n alexxapp --timeout=120s
kubectl wait --for=condition=ready pod -l app=prometheus -n monitoring --timeout=90s
kubectl wait --for=condition=ready pod -l app=grafana -n monitoring --timeout=90s

echo "Starting port forwarding..."
kubectl port-forward service/prometheus 9090:9090 -n monitoring &
sleep 2
kubectl port-forward service/grafana 3000:3000 -n monitoring &
sleep 2
kubectl port-forward service/nfstream-service 5201:5201 -n alexxapp &
sleep 2

echo "Grafana & Prometheus running"

echo "Starting iperf3"
kubectl exec -n alexxapp nfstream-pod -c xapp -- iperf3 -s -p 5201 &

# pods running
echo "Showing running pods..."
kubectl get pods -n alexxapp
