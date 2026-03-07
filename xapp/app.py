import numpy as np
import onnxruntime as ort
import json
import time
from nfstream import NFStreamer
from prometheus_client import start_http_server, Gauge, Counter

sess = ort.InferenceSession("./rf_model.onnx")
streamer = NFStreamer(source="any", idle_timeout=1, active_timeout=5)


with open("./features.json", "r") as f:
    feature_order = json.load(f)


def extract_features(flow):
    value_by_name = {
        "protocol": getattr(flow, "protocol", None),
        "duration": getattr(flow, "duration", None),
        "fwd_packets": getattr(flow, "fwd_packets", None),
        "bwd_packets": getattr(flow, "bwd_packets", None),
        "fwd_bytes": getattr(flow, "fwd_bytes", None),
        "bwd_bytes": getattr(flow, "bwd_bytes", None),
        "pkt_len_mean": getattr(flow, "pkt_len_mean", None),
        "pkt_len_std": getattr(flow, "pkt_len_std", None),
        "fwd_pkt_len_mean": getattr(flow, "fwd_pkt_len_mean", None),
        "fwd_pkt_len_std": getattr(flow, "fwd_pkt_len_std", None),
        "bwd_pkt_len_mean": getattr(flow, "bwd_pkt_len_mean", None),
        "bwd_pkt_len_std": getattr(flow, "bwd_pkt_len_std", None),
        "iat_mean": getattr(flow, "iat_mean", None),
        "fwd_iat_mean": getattr(flow, "fwd_iat_mean", None),
        "bwd_iat_mean": getattr(flow, "bwd_iat_mean", None),
        "syn_count": getattr(flow, "syn_count", None),
        "fin_count": getattr(flow, "fin_count", None),
        "psh_count": getattr(flow, "psh_count", None),
        "ack_count": getattr(flow, "ack_count", None),
    }

    row = [value_by_name[name] for name in feature_order]
    return np.asarray([row], dtype=np.float32)

LATENCY = Gauge('xapp_inference_latency_ms', 'Time taken for prediction')
FLOW_COUNT = Counter('xapp_flows_total', 'Total number of flows processed')
PREDICTION = Gauge('xapp_last_prediction', 'Last prediction value')
start_http_server(8000)

for flow in streamer:
    print(f"Flow req {flow.id}: {flow.requested_server_name}")
    FLOW_COUNT.inc()
    start_time = time.time()
    features = extract_features(flow)
    input_name = sess.get_inputs()[0].name
    output_name = sess.get_outputs()[0].name
    prediction = sess.run([output_name], {input_name: features})
    print((time.time() - start_time) * 1000)
    LATENCY.set((time.time() - start_time) * 1000)
    print("Prediction:", prediction[0][0])
    PREDICTION.set(prediction[0][0])