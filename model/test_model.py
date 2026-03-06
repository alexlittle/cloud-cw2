import numpy as np
import onnxruntime as ort


sess = ort.InferenceSession("../xapp/rf_model.onnx")

features = {
    "src_port": 12345,
    "dst_port": 80,
    "protocol": 6,
    "bidirectional_packets": 10,
    "bidirectional_bytes": 1000,
    "bidirectional_duration_ms": 500,
}

input_data = np.array([
    [
        features["src_port"],
        features["dst_port"],
        features["protocol"],
        features["bidirectional_packets"],
        features["bidirectional_bytes"],
        features["bidirectional_duration_ms"],
    ]
], dtype=np.float32)

input_name = sess.get_inputs()[0].name
output_name = sess.get_outputs()[0].name
prediction = sess.run([output_name], {input_name: input_data})

print("Prediction:", prediction[0][0])