# Cloud Computing Coursework 2

## Alex Little - nqxs0665


## Directory/File Overview:

```
- kubernetes/ - k8s scripts for loading monitor and xApp
    ├ monitoring.yaml
    └ xapp-dev.yaml
- model/ - for training/creating model that will be used for classifying network traffic types

    └ train_rf_model.py - script to train Random Forest model
- xapp/ - the VNF to be deployed
    ├ app.py
    ├ Dockerfile
    ├ features.json
    ├ requirements.txt - requirements needed just for the function
    └ rf_model.onnx - Random Forest model in ONNX format
- dashboard.json
- GenAI_troubleshooting.md
- requirements.txt - requirements for all components, including the model
- rebuild-minikube.sh
- requirements.txt - requirements needed for model training and the xApp
```


## Install


## Development


