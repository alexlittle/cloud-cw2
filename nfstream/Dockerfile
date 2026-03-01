FROM python:3.10-slim

# ensure NFstream dependencies are installed
RUN apt-get update && apt-get install -y \
    build-essential \
    libpcap-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]