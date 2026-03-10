# Cloud Computing Coursework 2

## Alex Little - nqxs0665


## Directory/File Overview:

```
- dashboard/ - json files to easily recreate the Grafana dashboards
    ├ k3s.json
    └ minikube.json
- kubernetes/ - K8s scripts for loading monitor and xApp
    ├ monitoring.yaml - K8s configuration for Prometheus and Grafana 
    ├ testing.yaml - K8s configuration for running the tcpreplay 
    └ xapp-dev.yaml
- model/ - for training/creating model that will be used for classifying network traffic types
    ├ process_data.py
    └ train_rf_model.py - script to train Random Forest model
- xapp/ - the VNF to be deployed
    ├ app.py
    ├ Dockerfile
    ├ features.json
    ├ requirements.txt - requirements needed just for the function
    └ rf_model.onnx - Random Forest model in ONNX format
- GenAI_troubleshooting.md - usage of CoPilot for this project
- rebuild-k3s.sh - shell script to rebuild the k3s environment from scratch
- rebuild-minikube.sh - shell script to rebuild the MiniKube environment from scratch
- requirements.txt - requirements needed for model training and the xApp
- start-minikube.sh - shell script to restart minikube and port-forwarding
```

## Running tests

Start test container: `kubectl apply -f kubernetes/testing.yaml`

Enter test container shell: `kubectl exec -it traffic-gen -n alexxapp -- bash`

Run tcpreplay (eg): `tcpreplay -i eth0 --mbps=100 --loop=0 /pcaps/bigflows.pcap`


## Training Data Source

The CIC-IDS2017 (Flow-Based Intrusion Detection Dataset, CIC @UNB Fredericton) dataset used for training the model is not included here, but can be downloaded from https://www.kaggle.com/datasets/dhoogla/cicids2017/data