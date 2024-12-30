# MQTT Broker for [PhoneGetter](https://github.com/PavelFr8/PhoneGetter)

Этот проект реализует простой брокер команд на основе MQTT с Flask для отправки команд 
на устройства через MQTT. Сервер подписывается на MQTT-темы, связанные с устройствами, 
и отправляет ответы с обновлениями статуса. Система предназначена для простого взаимодействия 
с IoT-устройствами(ESP8266) через MQTT.

## API Эндпоинты

```bash
curl -X POST http://127.0.0.1:5000/send_command -H "Content-Type: application/json" -d '{
  "device_api_token": "1234",
  "cell_id": 12}
```

Отправив JSON с токеном устройства и деталями команды. Команда будет опубликована в соответствующую MQTT-тему.

#### Пример тела запроса:

```json
{
  "device_api_token": "1234",
  "cell_id": 1
}
