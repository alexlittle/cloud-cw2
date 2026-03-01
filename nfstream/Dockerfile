FROM python:3.10-slim

# ensure NFstream dependencies are installed
RUN apt-get update && apt-get install -y \
    build-essential \
    libpcap-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# install requirements
RUN pip install --no-cache-dir -r requirements

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]