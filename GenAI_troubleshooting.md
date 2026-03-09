# GenAI troubleshooting

Information regarding use of Gen AI (CoPilot) in this project:


- switching between minikube and k3s - for k3s the config needs to be reset
## Issue 1: Configuring the prometheus and grafana monitoring and connecting to the datasource.

**Problem**: No data showing in panel

**Prompt**:

**Suggested Solution**:

**Did it work?** Yes


## Issue 2: Error with port forwarding

**Problem**: After running the startup shell scripts (for either MiniKube or k3s), I had error messages similar to "an error occurred forwarding 3000 -> 3000"


**Prompt**: With my shell script (attached), I get the error message: "E0308 11:20:50.779678   42255 portforward.go:424] "Unhandled Error" err="an error occurred forwarding 3000 -> 3000: error forwarding port 3000 to pod 47913a71ad379facb676f0c255a3533c645d22275a683d4cf559eb60f7198df3, uid : failed to execute portforward in network namespace \"/var/run/netns/cni-d640da59-037a-5d99-d30d-1720c4f632b5\": failed to connect to localhost:3000 inside namespace \"47913a71ad379facb676f0c255a3533c645d22275a683d4cf559eb60f7198df3\", IPv4: dial tcp4 127.0.0.1:3000: connect: connection refused IPv6 dial tcp6: address localhost: no suitable address found "

**Suggested Solution**: Suggested adding: "kubectl wait --for=condition=ready pod -l app=prometheus -n monitoring --timeout=90s
kubectl wait --for=condition=ready pod -l app=grafana -n monitoring --timeout=90s" and some "sleep" commands into my startup script

**Did it work?** Yes, although using a sleep command doesn't seem like a great fix

## Issue 3: 

**Problem**:


**Prompt**:

**Suggested Solution**:

**Did it work?**


## Issue 4: 

**Problem**:


**Prompt**:

**Suggested Solution**:

**Did it work?**


## Issue 5: 

**Problem**:


**Prompt**:

**Suggested Solution**:

**Did it work?**

