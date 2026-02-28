from nfstream import NFStreamer

streamer = NFStreamer(source="eth0", idle_timeout=1, active_timeout=5)

for flow in streamer:
    print(flow)