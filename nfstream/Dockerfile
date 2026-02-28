FROM python:3.12-slim

# ensure NFstream dependencies are installed
RUN apt-get update && apt-get install -y \
    build-essential \
    libpcap-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# install nfstream
RUN pip install --no-cache-dir nfstream

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]