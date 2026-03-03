# Train with CIC-IDS2017 data
import pandas as pd

files = [
    "./data/Benign-Monday-no-metadata.parquet",
    "./data/Botnet-Friday-no-metadata.parquet",
    "./data/Bruteforce-Tuesday-no-metadata.parquet",
    "./data/DDoS-Friday-no-metadata.parquet",
    "./data/DoS-Wednesday-no-metadata.parquet",
    "./data/Infiltration-Thursday-no-metadata.parquet",
    "./data/Portscan-Friday-no-metadata.parquet",
    "./data/WebAttacks-Thursday-no-metadata.parquet",
]

dfs = [pd.read_parquet(f) for f in files]

df = pd.concat(dfs, ignore_index=True)


# map CIC-IDS2017 col names to NFStream flow names
to_nfstream = {
    "Protocol": "protocol",
    "Flow Duration": "duration",
    "Total Fwd Packets": "fwd_packets",
    "Total Backward Packets": "bwd_packets",
    "Fwd Packets Length Total": "fwd_bytes",
    "Bwd Packets Length Total": "bwd_bytes",
    "Fwd Packet Length Mean": "fwd_pkt_len_mean",
    "Fwd Packet Length Std": "fwd_pkt_len_std",
    "Bwd Packet Length Mean": "bwd_pkt_len_mean",
    "Bwd Packet Length Std": "bwd_pkt_len_std",
    "Packet Length Mean": "pkt_len_mean",
    "Packet Length Std": "pkt_len_std",
    "Flow IAT Mean": "iat_mean",
    "Fwd IAT Mean": "fwd_iat_mean",
    "Bwd IAT Mean": "bwd_iat_mean",
    "SYN Flag Count": "syn_count",
    "FIN Flag Count": "fin_count",
    "PSH Flag Count": "psh_count",
    "ACK Flag Count": "ack_count",
}

# rename columns
existing_renames = {src: dst for src, dst in to_nfstream.items() if src in df.columns}
nf = df.rename(columns=existing_renames).copy()

# total_packets
if {"fwd_packets", "bwd_packets"}.issubset(nf.columns):
    nf["total_packets"] = nf["fwd_packets"] + nf["bwd_packets"]

# total_bytes
if {"fwd_bytes", "bwd_bytes"}.issubset(nf.columns):
    nf["total_bytes"] = nf["fwd_bytes"] + nf["bwd_bytes"]

nfstream_like_cols = [
    "protocol", "duration",
    "fwd_packets", "bwd_packets",
    "fwd_bytes", "bwd_bytes",
    "pkt_len_mean", "pkt_len_std",
    "fwd_pkt_len_mean", "fwd_pkt_len_std",
    "bwd_pkt_len_mean", "bwd_pkt_len_std",
    "iat_mean", "fwd_iat_mean", "bwd_iat_mean",
    "syn_count", "fin_count", "psh_count", "ack_count", "Label"
]
nf = nf[[c for c in nfstream_like_cols if c in nf.columns]]

print(nf["Label"].value_counts())
# map to 1=Benign and anything malicious as 0
nf["Label"] = (nf["Label"] == "Benign").astype(int)

nf.to_csv("./data/CIC-IDS2017.csv", index=False)

