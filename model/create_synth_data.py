import pandas as pd
import numpy as np


def generate_synth_data(n_samples=50000):
    np.random.seed(42)
    data = []

    # actions and weightings
    # 0 - targetA
    # 1 - targetB
    # 2 - malicious
    actions = [0, 1, 2]
    weights = [0.60, 0.35, 0.05]

    for _ in range(n_samples):
        label = np.random.choice(actions, p=weights)

        targetA_load = np.round(np.random.uniform(20, 95),2)
        targetB_load = np.round(np.random.uniform(20, 95),2)

        if label == 2:
            # if malicious
            if np.random.random() < 0.6:
                # for DDOS type
                entropy = np.round(np.random.uniform(0.05, 0.2),2)
                packet_count = np.random.randint(2000, 5000)
                avg_pkt_size = np.random.randint(40, 80)
            else:
                # for scanning
                entropy = np.round(np.random.uniform(0.3, 0.7), 2)
                packet_count = np.random.randint(80, 900)
                avg_pkt_size = np.random.randint(50, 1500)
        else:
            # estimates for normal traffic
            entropy = np.round(np.random.uniform(0.1, 0.4),2)
            packet_count = np.random.randint(100, 800)
            avg_pkt_size = np.random.randint(500, 1500)

            # add some noise so not a straight if/then on the load
            # use a base load, plus some extra latency if high load and penalise for bigger packets
            baseA_load = 10
            baseB_load = 11
            latency_factor = 0.2
            packet_factor = 0.005
            noise = np.random.normal(0, 0.5)

            totalA_load = baseA_load + (latency_factor * targetA_load) + (packet_factor * targetA_load) + noise
            totalB_load = baseB_load + (latency_factor * targetB_load) + (packet_factor * targetB_load) + noise

            # decide where to route
            if targetA_load > 95:
                label = 1
            elif totalA_load < totalB_load:
                label = 0
            else:
                label = 1

        data.append([entropy, packet_count, avg_pkt_size, targetA_load, targetB_load, label])

    return pd.DataFrame(data, columns=['entropy', 'packet_count', 'pkt_size', 'targetA_load', 'targetB_load', 'action'])


df = generate_synth_data()
df.to_csv("synth_traffic_data.csv", index=False)