#!/bin/bash
# For testing miniKube setup


#./rebuild-minikube.sh


# Test 1 - Basic setup check
iperf3 -c localhost -p 5201 -t 30 -P 1 -b 10M


# Test 2 - Light
iperf3 -c localhost -p 5201 -t 60 -P 5 -b 10M


# Test 3 - medium
iperf3 -c localhost -p 5201 -t 60 -P 10 -b 20M


# Test 4 - heavy
iperf3 -c localhost -p 5201 -t 60 -P 20 -b 50M


#Test 5 - unrestricted
iperf3 -c localhost -p 5201 -t 120 -P 20

# Test 6 - sustained
iperf3 -c localhost -p 5201 -t 600 -P 10 -b 20M