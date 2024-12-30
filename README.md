# MQTT Broker for [PhoneGetter](https://github.com/PavelFr8/PhoneGetter)
This project implements a simple command broker based on MQTT with Flask to send 
commands to devices via MQTT. The server subscribes to MQTT topics related to devices 
and sends responses with status updates. The system is designed for simple interaction 
with IoT devices (ESP8266) through MQTT.

## API Endpoints

```bash
curl -X POST http://127.0.0.1:5000/send_command -H "Content-Type: application/json" -d '{
  "device_api_token": "1234",
  "cell_id": 12}
```

Send a JSON with the device API token and command details. 
The command will be published to the corresponding MQTT topic.

#### Пример тела запроса:

```json
{
  "device_api_token": "1234",
  "cell_id": 1
}
