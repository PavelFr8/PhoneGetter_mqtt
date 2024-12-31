# MQTT Broker for [PhoneGetter](https://github.com/PavelFr8/PhoneGetter)

This project implements a simple command broker based on MQTT with Flask to send commands 
to devices via MQTT. The server subscribes to MQTT topics related to devices and sends responses
with status updates. The system is designed for simple interaction with IoT devices 
(e.g., ESP8266) through MQTT.

## Libraries

Install the required libraries with pip:

```bash
pip install -r requirements.txt
```

## Endpoints

### `POST /send_command`

Send a JSON payload with the device API token and command details. The command will be published to the corresponding MQTT topic.

#### Example Request:

```bash
curl -X POST http://127.0.0.1:5000/send_command -H "Content-Type: application/json" -d '{
  "device_api_token": "1234",
  "cell_id": 12
}'
```

#### Example Request Body:

```json
{
  "device_api_token": "device_api_token",
  "cell_id": 1234
}
```

#### Response:

```json
{
  "status": "success",
  "message": "Command sent successfully."
}
```

## How to Run the Broker

1. Write your broker data in .env (check .env_example)

2. Run Flask

```bash
flask run
```