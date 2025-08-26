# Projeto Smart City IoT — Guia Passo a Passo

Este repositório contém uma base **pronta** para emular uma rede IoT heterogênea com 3 dispositivos, um broker MQTT, um controlador (cloud) e monitoramento com **Prometheus + Grafana**.

## 1) Pré-requisitos (Ubuntu Desktop 22.04+)

```bash
# 1) Atualizar pacotes
sudo apt update && sudo apt -y upgrade

# 2) Instalar Docker Engine + Compose plugin
sudo apt -y install ca-certificates curl gnupg lsb-release
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg]   https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" |   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 3) Permitir seu usuário usar Docker sem sudo (faça logout/login após)
sudo usermod -aG docker $USER
```

Verifique:
```bash
docker run --rm hello-world
docker compose version
```

## 2) Subir a arquitetura

Na raiz do projeto:

```bash
docker compose up -d --build
docker ps
```

Serviços:
- **Grafana:** http://localhost:3000 (admin / admin)
- **Prometheus:** http://localhost:9090
- **cAdvisor:** http://localhost:8080

O Grafana já vem provisionado com a fonte de dados Prometheus e o dashboard **Smart City IoT — Overview**.

## 3) O que está sendo emulado

- **3 dispositivos** (containers) com perfis distintos e **NETEM (tc)** por container para delay/jitter/loss:
  - `device_a` → `air_quality` (10s, ~200B, 50ms delay, 0.1% loss)
  - `device_b` → `street_light` (5s, ~150B, 30ms delay, 0.05% loss)
  - `device_c` → `traffic_cam` (1s, ~5KB, 15ms delay, 0.01% loss)

- **Broker MQTT (Mosquitto)** em `mosquitto:1883`

- **Controller (cloud)**: assina `smartcity/#`, mede **latência fim-a-fim** (device→controller) e expõe métricas Prometheus:
  - `iot_messages_received_total{device,app,topic}`
  - `iot_e2e_latency_seconds_bucket/sum/count` (histograma)

- **Cada dispositivo** expõe:
  - `iot_messages_sent_total{device,app,topic}`

- **Prometheus** coleta métricas do controller, dos devices, do **cAdvisor** (CPU/RAM/Rede dos containers) e do **node-exporter** (host).

## 4) Ajustar cenários (apps e dispositivos)

Edite `docker-compose.yml`:
- **Frequência**: `INTERVAL_SECONDS`
- **Tamanho dos dados** simulados: `PAYLOAD_BYTES`
- **Emulação de rede**: `NETEM_DELAY_MS`, `NETEM_JITTER_MS`, `NETEM_LOSS_PCT`
- **Tópicos e nomes**: `TOPIC`, `DEVICE_NAME`, `APP`

Recrie os serviços que mudar:
```bash
docker compose up -d --build device_a device_b device_c
```

## 5) Onde ver as métricas no Grafana

Dashboard: **Smart City IoT — Overview**
- **E2E Latency p95 by App**: latência (p95) por aplicação
- **Throughput (msg/s)**: taxa de mensagens recebidas por aplicação
- **Messages Sent (msg/s)**: taxa de envio por dispositivo
- **CPU/Mem/Net**: métricas por container (via cAdvisor)

Você pode duplicar e editar o dashboard para criar:
- Latência por **dispositivo**
- **Alertas** (p95 > 0.5s, perda aparente etc.)
- Tráfego por tópico (via recebimento por app)

## 6) Logs e validação

```bash
docker logs -f controller
docker logs -f device_a
docker logs -f device_b
docker logs -f device_c
```

## 7) Parar e limpar

```bash
docker compose down
# Para remover volumes (dados Grafana), adicione -v
docker compose down -v
```

## 8) Extensões (opcional)

- Adicionar **novo dispositivo**: copie uma pasta de device, ajuste variáveis, adicione ao compose.
- Incluir **Mininet/NetEm no host** para topologias mais complexas.
- Adicionar **mosquitto-exporter** para métricas do broker.
- Usar **CoAP/HTTP** em containers alternativos das aplicações para comparar protocolos.

Bom estudo! 🚀
