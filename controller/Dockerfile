
FROM python:3.11-slim

WORKDIR /app
COPY controller.py /app/controller.py

RUN pip install --no-cache-dir paho-mqtt prometheus-client

CMD ["python", "/app/controller.py"]
