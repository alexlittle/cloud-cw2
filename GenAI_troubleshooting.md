# GenAI troubleshooting

Information regarding use of Gen AI (CoPilot) in this project:


## Issue 1: Configuring the prometheus and grafana monitoring and connecting to the datasource.

**Problem**: No data showing in panel for CPU and RAM

**Prompt**: In my K3s setup I don't see any data showing for CPU and RAM, but this is working when viewed in my Minikube environment. 
The query I'm using is: 
```
sum(container_memory_working_set_bytes{namespace="alexxapp", pod="nfstream-pod", container=""}) by (pod)/1024/1024
```

**Suggested Solution**: In K3s the query needs to specify the container:

```
sum(container_memory_working_set_bytes{namespace="alexxapp", pod="nfstream-pod", container="xapp"}) by (pod)/1024/1024
```

What was used previously explicitly filtered for containers with empty name, Minikube is more forgiving on this than k3s

**Did it work?** Yes, similarly with the other queries, I needed to make sure that the container was specified for 


## Issue 2: Error with port forwarding

**Problem**: After running the startup shell scripts (for either MiniKube or k3s), I had error messages similar to "an error occurred forwarding 3000 -> 3000"


**Prompt**: With my shell script (attached), I get the error message: "E0308 11:20:50.779678   42255 portforward.go:424] "Unhandled Error" err="an error occurred forwarding 3000 -> 3000: error forwarding port 3000 to pod 47913a71ad379facb676f0c255a3533c645d22275a683d4cf559eb60f7198df3, uid : failed to execute portforward in network namespace \"/var/run/netns/cni-d640da59-037a-5d99-d30d-1720c4f632b5\": failed to connect to localhost:3000 inside namespace \"47913a71ad379facb676f0c255a3533c645d22275a683d4cf559eb60f7198df3\", IPv4: dial tcp4 127.0.0.1:3000: connect: connection refused IPv6 dial tcp6: address localhost: no suitable address found "

**Suggested Solution**: Suggested adding: 
```
kubectl wait --for=condition=ready pod -l app=prometheus -n monitoring --timeout=90s
kubectl wait --for=condition=ready pod -l app=grafana -n monitoring --timeout=90s" 
```
and some "sleep" commands into my startup script

**Did it work?** Yes, although using a sleep command doesn't seem like a great fix

## Issue 3: k3s fails to start

**Problem**: Starting k3s fails, but was working previously

**Prompt**: Why is k3s failing to start, it was working correctly before? Here is the message I get: E0311 19:02:44.170959  519149 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"http://localhost:8080/api?timeout=32s\": dial tcp 127.0.0.1:8080: connect: connection refused

**Suggested Solution**: Need to reset the config file for k3s after using Minikube and going back to running k3s, using:

```
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $(id -u):$(id -g) ~/.kube/config
export KUBECONFIG=~/.kube/config
```

**Did it work?**: Yes


## Issue 4: pcap files not being found for testing

**Problem**: File not found error when running tcpreplay on Minikube

**Prompt**: When I run this command on Minikube I get a file not found error, `tcpreplay -i eth0 --mbps=1000 --loop=0 /pcaps/bigflows.pcap` although in K3s the file is found no problem (with attached testing.yaml file). Here is the specific error: 



**Suggested Solution**: For Minikube the mount path needs to be initiated differently as it is the host machine, in k3s your laptop is the host. So start Minikube with flag "--mount --mount-string="/home/alex/Downloads/pcap:/home/alex/Downloads/pcap"

**Did it work?** Yes - there were several options for how to solve this, but the one used above seemed the easiest/quickest for what was needed


