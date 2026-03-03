
import pandas as pd

df = pd.read_parquet("data/Bruteforce-Tuesday-no-metadata.parquet")

print(df.columns)
print(df["Label"].value_counts())

'''
NFlow(id=10,
      expiration_id=0,
      src_ip=10.244.0.3,
      src_mac=12:71:be:2f:88:1c,
      src_oui=12:71:be,
      src_port=48105,
      dst_ip=10.96.0.10,
      dst_mac=5a:84:37:c4:57:27,
      dst_oui=5a:84:37,
      dst_port=53,
      protocol=17,
      ip_version=4,
      vlan_id=0,
      tunnel_id=0,
      bidirectional_first_seen_ms=1772558742379,
      bidirectional_last_seen_ms=1772558742379,
      bidirectional_duration_ms=0,
      bidirectional_packets=4,
      bidirectional_bytes=594,
      src2dst_first_seen_ms=1772558742379,
      src2dst_last_seen_ms=1772558742379,
      src2dst_duration_ms=0,
      src2dst_packets=2,
      src2dst_bytes=204,
      dst2src_first_seen_ms=1772558742379,
      dst2src_last_seen_ms=1772558742379,
      dst2src_duration_ms=0,
      dst2src_packets=2,
      dst2src_bytes=390,
      application_name=DNS,
      application_category_name=Network,
      application_is_guessed=0,
      application_confidence=6,
      requested_server_name=debian.map.fastlydns.net.svc.cluster.local,
      client_fingerprint=,
      server_fingerprint=,
      user_agent=,
      content_type=)
      
      
['Protocol', 'Flow Duration', 'Total Fwd Packets',
       'Total Backward Packets', 'Fwd Packets Length Total',
       'Bwd Packets Length Total', 'Fwd Packet Length Max',
       'Fwd Packet Length Min', 'Fwd Packet Length Mean',
       'Fwd Packet Length Std', 'Bwd Packet Length Max',
       'Bwd Packet Length Min', 'Bwd Packet Length Mean',
       'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s',
       'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min',
       'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max',
       'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std',
       'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags',
       'Fwd URG Flags', 'Bwd URG Flags', 'Fwd Header Length',
       'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s',
       'Packet Length Min', 'Packet Length Max', 'Packet Length Mean',
       'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count',
       'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count',
       'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count', 'Down/Up Ratio',
       'Avg Packet Size', 'Avg Fwd Segment Size', 'Avg Bwd Segment Size',
       'Fwd Avg Bytes/Bulk', 'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate',
       'Bwd Avg Bytes/Bulk', 'Bwd Avg Packets/Bulk', 'Bwd Avg Bulk Rate',
       'Subflow Fwd Packets', 'Subflow Fwd Bytes', 'Subflow Bwd Packets',
       'Subflow Bwd Bytes', 'Init Fwd Win Bytes', 'Init Bwd Win Bytes',
       'Fwd Act Data Packets', 'Fwd Seg Size Min', 'Active Mean', 'Active Std',
       'Active Max', 'Active Min', 'Idle Mean', 'Idle Std', 'Idle Max',
       'Idle Min', 'Label']



mapping = {
    "protocol": flow.protocol,
    "src_port": flow.src_port,
    "dst_port": flow.dst_port,
    "duration": flow.duration,
    "total_packets": flow.total_packets,
    "total_bytes": flow.total_bytes,
    "fwd_packets": flow.fwd_packets,
    "bwd_packets": flow.bwd_packets,
    "pkt_len_mean": flow.pkt_len_mean,
    "pkt_len_std": flow.pkt_len_std,
    "fwd_iat_mean": flow.fwd_iat_mean,
    "bwd_iat_mean": flow.bwd_iat_mean,
}

'''

import numpy as np

# Your CIC-IDS2017-like DataFrame
# df = ...

EPS = 1e-6  # avoid division by zero

# 1) Inverse mapping: from your dataset columns to NFStream-style names
to_nfstream = {
    # identifiers / metadata
    "Protocol": "protocol",
    "Flow Duration": "duration",

    # packet/byte counters (directional)
    "Total Fwd Packets": "fwd_packets",
    "Total Backward Packets": "bwd_packets",
    "Fwd Packets Length Total": "fwd_bytes",
    "Bwd Packets Length Total": "bwd_bytes",

    # packet length stats
    "Fwd Packet Length Mean": "fwd_pkt_len_mean",
    "Fwd Packet Length Std": "fwd_pkt_len_std",
    "Bwd Packet Length Mean": "bwd_pkt_len_mean",
    "Bwd Packet Length Std": "bwd_pkt_len_std",
    "Packet Length Mean": "pkt_len_mean",
    "Packet Length Std": "pkt_len_std",

    # IAT stats (overall + directional)
    "Flow IAT Mean": "iat_mean",
    "Fwd IAT Mean": "fwd_iat_mean",
    "Bwd IAT Mean": "bwd_iat_mean",

    # flags (if present in your dataset)
    "SYN Flag Count": "syn_count",
    "FIN Flag Count": "fin_count",
    "PSH Flag Count": "psh_count",
    "ACK Flag Count": "ack_count",
}

# 2) Only rename columns that actually exist in df
existing_renames = {src: dst for src, dst in to_nfstream.items() if src in df.columns}
nf = df.rename(columns=existing_renames).copy()

# 3) Derive NFStream-like convenience fields where possible

# total_packets = fwd + bwd
if {"fwd_packets", "bwd_packets"}.issubset(nf.columns):
    nf["total_packets"] = nf["fwd_packets"] + nf["bwd_packets"]

# total_bytes = fwd + bwd
if {"fwd_bytes", "bwd_bytes"}.issubset(nf.columns):
    nf["total_bytes"] = nf["fwd_bytes"] + nf["bwd_bytes"]

# Rates similar to what you'd compute from NFStream outputs
if {"total_bytes", "duration"}.issubset(nf.columns):
    nf["bytes_per_second"] = nf["total_bytes"] / np.maximum(nf["duration"], EPS)  # optional
if {"total_packets", "duration"}.issubset(nf.columns):
    nf["packets_per_second"] = nf["total_packets"] / np.maximum(nf["duration"], EPS)  # optional

# 4) Keep only the NFStream-style columns you care about (adjust as needed)
nfstream_like_cols = [
    "protocol", "duration",
    "fwd_packets", "bwd_packets",
    "fwd_bytes", "bwd_bytes",
    "pkt_len_mean", "pkt_len_std",
    "fwd_pkt_len_mean", "fwd_pkt_len_std",
    "bwd_pkt_len_mean", "bwd_pkt_len_std",
    "iat_mean", "fwd_iat_mean", "bwd_iat_mean",
    "syn_count", "fin_count", "psh_count", "ack_count",
    # convenience fields
    "total_packets", "total_bytes", "packets_per_second", "bytes_per_second",
]
nf = nf[[c for c in nfstream_like_cols if c in nf.columns]]

