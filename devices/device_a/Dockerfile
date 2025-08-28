###################################################################################################
FROM prom/node-exporter:latest as builder

FROM python:3.9-slim

WORKDIR /app

# Copia o binário do node_exporter do estágio de build anterior
COPY --from=builder /bin/node_exporter /bin/node_exporter

# Instala o supervisor e as ferramentas de rede que já tínhamos
RUN apt-get update && apt-get install -y supervisor iproute2 iputils-ping && rm -rf /var/lib/apt/lists/*

RUN pip install paho-mqtt

# Copia os scripts da nossa aplicação
COPY app.py .

# Copia o novo arquivo de configuração do supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expõe a porta 9100, onde o node_exporter irá servir as métricas
EXPOSE 9100

# O supervisor agora é o comando principal que gerencia os outros processos
CMD ["/usr/bin/supervisord"]