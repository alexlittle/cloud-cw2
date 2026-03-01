import numpy as np
import onnxruntime as ort
from nfstream import NFStreamer

sess = ort.InferenceSession("./rf_model.onnx")
streamer = NFStreamer(source="eth0", idle_timeout=1, active_timeout=5)

def extract_features(flow):
    return np.array([
    [
        flow.src_port,
        flow.dst_port,
        flow.protocol,
        flow.bidirectional_packets,
        flow.bidirectional_bytes,
        flow.bidirectional_duration_ms,
    ]
    ], dtype = np.float32)


for flow in streamer:
    features = extract_features(flow)
    input_name = sess.get_inputs()[0].name
    output_name = sess.get_outputs()[0].name
    prediction = sess.run([output_name], {input_name: features})

    print("Prediction:", prediction[0][0])