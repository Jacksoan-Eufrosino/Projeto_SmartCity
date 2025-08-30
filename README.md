<h1 align="center">Projeto SmartCity</h1>

<p align="center">
Emulação e monitoramento de redes IoT heterogêneas em um ambiente de Smart City, com dispositivos simulando qualidade do ar, iluminação pública e tráfego, usando Mininet, Docker, Prometheus e Grafana.
</p>


## 🧔🏻 Equipe

- **Jacksoan Eufrosino de Freitas** — 20231380018 
- **Antony César Pereira de Araújo** — 20231380013  
- **Gabriel Lavor de Albuquerque** — 20231380037

## 📝 Resumo

**Projeto_SmartCity** é uma base pronta para **emular e monitorar redes IoT heterogêneas** em um ambiente de cidade inteligente.  
A solução integra **Mininet** para simulação de rede, **Docker** para conteinerização dos dispositivos, além de **Prometheus + Grafana** para coleta e visualização de métricas.

O projeto conta com **três dispositivos IoT representativos** de aplicações reais em Smart Cities:

- 🌬️ **Air-Quality (PurpleAir PA-II):** mede PM2.5, PM10, temperatura, umidade e AQI, usado em monitoramento ambiental.  
- 💡 **Street Light (Philips CityTouch):** controlador de postes inteligentes com funções de consumo, falhas e agendamento.  
- 🚦 **Traffic Cam (Axis Q1700-LE):** câmera IP para leitura automática de placas (ANPR) e monitoramento de tráfego.  

---

## 🗺️ Topologia

A topologia do Projeto SmartCity representa a estrutura de comunicação entre os dispositivos IoT e o monitoramento central:

🌬️ **Air-Quality**, 💡 **Street Light** e 🚦 **Traffic Cam**: são os três dispositivos IoT simulados, representando sensores ambientais, iluminação pública e câmeras de tráfego. Cada um funciona em um contêiner Docker isolado.

📶 **Router**: centraliza a comunicação entre os dispositivos IoT e os sistemas de monitoramento. Funciona como um ponto de roteamento da rede emulada.

📊 **Prometheus**: recebe métricas e dados de todos os dispositivos via rede. Atua como banco de dados de séries temporais para monitoramento.

📈 **Grafana**: acessa os dados do Prometheus para gerar dashboards e visualizações em tempo real, permitindo análise rápida do estado da rede e dispositivos.

🔄 Fluxo de dados: todos os dispositivos enviam suas informações para o Router → Router encaminha para o Prometheus → Prometheus disponibiliza os dados para o Grafana.

<p align="center">
  <img src="https://github.com/antonyllz/IpApi/blob/main/img01.png?raw=true" alt="Projeto SmartCity" width="600"/> 
</p>

---

## 💻 Ferramentas Utilizadas

- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg" width="22" height="22" /> **Linux**  
- <img src="https://prometheus.io/twitter-image.png?b370f6418ef38b42" width="22" height="22" /> **Prometheus**  
- <img src="https://cdn.iconscout.com/icon/free/png-256/free-grafana-logo-icon-svg-png-download-2944910.png" width="22" height="22" /> **Grafana**  
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="22" height="22" /> **Python**  
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="22" height="22" /> **Docker**  



## ⚡ Principais Funcionalidades

- 🌐 **Emulação de Dispositivos IoT**  
  Simulação de sensores inteligentes (qualidade do ar, iluminação pública e tráfego) com recursos de hardware limitados, próximos ao comportamento real.  

- 🛰️ **Emulação de Rede**  
  Criação de topologias no **Mininet**, aplicando condições reais de rede como latência, jitter e perda de pacotes.  

- 📊 **Monitoramento Centralizado**  
  Coleta automática de métricas com **Prometheus** e visualização em tempo real via **Grafana**, com possibilidade de alertas personalizados.  

- 📦 **Ambiente Conteinerizado**  
  Toda a infraestrutura (dispositivos, broker MQTT e serviços) roda em contêineres **Docker**, garantindo escalabilidade, isolamento e fácil replicação.  

- 🔄 **Comunicação via MQTT**  
  Troca de mensagens entre os dispositivos e o controlador em nuvem usando o protocolo **MQTT**, padrão em aplicações IoT.  


---
