
FROM python:3.11-slim

RUN apt-get update && apt-get install -y iproute2 iputils-ping && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY sensor.py /app/sensor.py
COPY entrypoint.sh /app/entrypoint.sh

RUN pip install --no-cache-dir paho-mqtt prometheus-client psutil

RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
