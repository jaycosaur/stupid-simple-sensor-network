# stupid-simple-sensor-network
#### An IoT sensor network of ESP32s, LoRa, micropython and microservices. ####

A stupid simple sensor network using highly available low cost sensors and devices. This project is an exercise to build a complex distrubted system using micropython, and to allow other developers a quickstart to get micropython IoT devices up and running.

## Hub and LoRa message broker

Hub features:
* A LoRa enabled Heltec HTIT-WB32LA connected to a local wifi network and capable of brokering LoRa node messages through an MQTT broker to be ingested by the cloud.
* Manages configuration updates to LoRa sensors (due to long sleep times).
* Conducts node health checks, status checks and periodic analytics.
* Has a simple 0.96 inch monochromatic 128 x 64 display that will display debugging, logging and device status / system health information.

## Nodes and Sensor Endpoints

Node features:
* A LoRa enabled Heltec HTIT-WB32LA which communicates to the local hub via LoRa.
* Handles devices configuration updates from local hub.
* Conducts self health checks and notifies local hub.
* Has a simple 0.96 inch monochromatic 128 x 64 display that will display debugging, logging and device status.
* Interfaced with modular sensors over i2c, spi, GPIO etc.

## MQTT Broker

TBD

## Cloud Services

TBD

## Analytic Services

TBD
