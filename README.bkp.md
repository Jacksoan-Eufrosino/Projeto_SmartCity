
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




1. Dispositivo de qualidade do ar (air-quality)

🛠️ Nome: PurpleAir PA-II
Descrição: Sensor IoT popular usado para medir partículas no ar (PM2.5, PM10).
Conectividade: Wi-Fi
Medições: PM2.5, PM10, temperatura, umidade, AQI (Air Quality Index)
Uso comum: Redes comunitárias de qualidade do ar, cidades inteligentes, pesquisas ambientais.
🌐 https://www.purpleair.com

| Especificação     | Detalhes                                    |
| ----------------- | ------------------------------------------- |
| **CPU**           | ESP8266 (SoC da Espressif)                  |
| **Memória RAM**   | \~160 KB (integrada no ESP8266)             |
| **Armazenamento** | Sem armazenamento persistente local         |
| **Sensores**      | Plantower PMS5003 (duplo) para PM2.5 / PM10 |
| **Conectividade** | Wi-Fi 2.4GHz                                |
| **Fonte**         | 5V DC via adaptador USB                     |






2. Dispositivo de monitoramento de iluminação pública (street_light)
🛠️ Nome: Philips CityTouch LightWave
Descrição: Controlador IoT para postes de luz inteligentes da Philips (Signify).
Conectividade: 3G/4G, ZigBee, LoRaWAN
Funções: Controle remoto de luminárias, monitoramento de consumo, falhas e agendamento de operação.
Uso comum: Cidades inteligentes com sistemas de iluminação adaptativa.
🌐 https://www.signify.com/global/lighting-services

| Especificação      | Detalhes                                                                |
| ------------------ | ----------------------------------------------------------------------- |
| **CPU**            | ARM Cortex-M3 (32-bit microcontrolador)                                 |
| **Memória RAM**    | 64 KB (estimado, varia por modelo)                                      |
| **Armazenamento**  | \~256 KB flash interno                                                  |
| **Conectividade**  | ZigBee, LoRaWAN, 3G/4G, NB-IoT (varia conforme versão)                  |
| **Energia**        | Alimentado pela própria luminária (AC, entre 110V–277V)                 |
| **Funções extras** | Medição de consumo de energia, detecção de falhas, escurecimento remoto |






3. Dispositivo de monitoramento de tráfego com câmera (traffic_cam)
🛠️ Nome: Axis Q1700-LE License Plate Camera
Descrição: Câmera IP IoT especializada em leitura de placas de veículos (ANPR).
Conectividade: Ethernet, PoE, suporta protocolos MQTT via gateways.
Funções: Gravação de vídeo, leitura automática de placas, monitoramento em tempo real.
Uso comum: Controle de tráfego, pedágios, entradas de cidades ou estacionamentos.
🌐 https://www.axis.com/products/axis-q1700-le

| Especificação     | Detalhes                                                              |
| ----------------- | --------------------------------------------------------------------- |
| **CPU**           | ARM Cortex-A9 dual-core (especificação típica em câmeras Axis)        |
| **Memória RAM**   | 512 MB                                                                |
| **Armazenamento** | 256 MB flash (interno), slot microSD para gravações                   |
| **Resolução**     | Full HD 1920x1080, sensor de alta sensibilidade para baixa iluminação |
| **Conectividade** | Ethernet (PoE, IPv4/IPv6, MQTT via gateways ou software externo)      |
| **Energia**       | Power over Ethernet (PoE IEEE 802.3af/at)                             |
