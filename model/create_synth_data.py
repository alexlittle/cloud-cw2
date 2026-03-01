import numpy as np
import pandas as pd
import random


# types of traffic and characteristics
classes = {
    "DNS": {
        "protocol": 17,  # UDP
        "src_port": lambda: np.random.randint(1024, 65535),
        "dst_port": 53,
        "bidirectional_packets": lambda: np.random.randint(2, 10),
        "bidirectional_bytes": lambda: np.random.randint(50, 500),
        "duration_ms": lambda: np.random.randint(10, 100),
        "application_name": "DNS",
    },
    "VoIP": {
        "protocol": 17,  # UDP
        "src_port": lambda: np.random.randint(1024, 65535),
        "dst_port": lambda: random.choice([5060, 5061, 16384, 32768]),
        "bidirectional_packets": lambda: np.random.randint(50, 500),
        "bidirectional_bytes": lambda: np.random.randint(1000, 50000),
        "duration_ms": lambda: np.random.randint(1000, 30000),
        "application_name": "VoIP",
    },
    "HTTP": {
        "protocol": 6,  # TCP
        "src_port": lambda: np.random.randint(1024, 65535),
        "dst_port": lambda: random.choice([80, 8080, 443]),
        "bidirectional_packets": lambda: np.random.randint(50, 5000),
        "bidirectional_bytes": lambda: np.random.randint(1000, 10000000),
        "duration_ms": lambda: np.random.randint(100, 10000),
        "application_name": "HTTP",
    },
    "Malicious": {
        "protocol": lambda: random.choice([6, 17]),  # TCP or UDP
        "src_port": lambda: np.random.randint(1024, 65535),
        "dst_port": lambda: random.choice([4444, 8080, 22, 80, 443, 3389]),
        "bidirectional_packets": lambda: np.random.randint(100, 10000),
        "bidirectional_bytes": lambda: np.random.randint(5000, 5000000),
        "duration_ms": lambda: np.random.randint(50, 5000),
        "application_name": "Malicious",
    },
    "SSH": {
        "protocol": 6,  # TCP
        "src_port": lambda: np.random.randint(1024, 65535),
        "dst_port": 22,
        "bidirectional_packets": lambda: np.random.randint(100, 5000),
        "bidirectional_bytes": lambda: np.random.randint(5000, 500000),
        "duration_ms": lambda: np.random.randint(1000, 60000),
        "application_name": "SSH",
    },
    "FTP": {
        "protocol": 6,  # TCP
        "src_port": lambda: np.random.randint(1024, 65535),
        "dst_port": lambda: random.choice([20, 21]),
        "bidirectional_packets": lambda: np.random.randint(100, 2000),
        "bidirectional_bytes": lambda: np.random.randint(10000, 1000000),
        "duration_ms": lambda: np.random.randint(500, 30000),
        "application_name": "FTP",
    },
}

# Generate synthetic data
def generate_data(class_name):
    cls = classes[class_name]
    return {
        "src_port": cls["src_port"]() if callable(cls["src_port"]) else cls["src_port"],
        "dst_port": cls["dst_port"]() if callable(cls["dst_port"]) else cls["dst_port"],
        "protocol": cls["protocol"]() if callable(cls["protocol"]) else cls["protocol"],
        "bidirectional_packets": cls["bidirectional_packets"](),
        "bidirectional_bytes": cls["bidirectional_bytes"](),
        "bidirectional_duration_ms": cls["duration_ms"](),
        "application_name": cls["application_name"],
    }

data = []
class_distribution = {
    "DNS": 0.2,
    "VoIP": 0.2,
    "HTTP": 0.25,
    "Malicious": 0.15,
    "SSH": 0.1,
    "FTP": 0.1,
}

for _ in range(50000):
    class_name = np.random.choice(
        list(class_distribution.keys()),
        p=list(class_distribution.values())
    )
    data.append(generate_data(class_name))

# convert to pandas and save csv
df = pd.DataFrame(data)
df.to_csv("synth_traffic.csv", index=False)

print("Generated synth traffic data csv file.")
