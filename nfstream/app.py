import joblib

from nfstream import NFStreamer

streamer = NFStreamer(source="eth0", idle_timeout=1, active_timeout=5)

def extract_features(flow):
    return {
        "src_port": flow.src_port,
        "dst_port": flow.dst_port,
        "protocol": flow.protocol,
        "bidirectional_packets": flow.bidirectional_packets,
        "bidirectional_bytes": flow.bidirectional_bytes,
        "bidirectional_duration_ms": flow.bidirectional_duration_ms,
    }

rf_model = joblib.load("rf_model.pkl")

for flow in streamer:
    features = extract_features(flow)
    prediction = rf_model.predict(features)
    print("Making prediction...")
    print(prediction)