#!/bin/bash

minikube start

kubectl wait --for=condition=ready pod/monitoring-stack -n monitoring --timeout=90s

kubectl port-forward pod/monitoring-stack 3000:3000 -n monitoring &
kubectl port-forward pod/monitoring-stack 9090:9090 -n monitoring &