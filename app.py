import os
import json
import logging
import threading
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from paho.mqtt.client import Client
from pydantic import BaseModel, ValidationError

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
MQTT_BROKER = os.environ.get("MQTT_BROKER")
MQTT_PORT = int(os.environ.get("MQTT_PORT"))
MQTT_USERNAME = os.environ.get("MQTT_USERNAME")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
MQTT_TOPIC_COMMAND = "device/{device_api_token}/command"
MQTT_TOPIC_RESPONSE = "device/{device_api_token}/response"

mqtt_client = Client()

def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe("device/+/command")

def on_message(client, userdata, msg):
    try:
        logger.info(f"Received message on topic {msg.topic}")
        device_api_token = msg.topic.split("/")[1]
        response_payload = {"status": "success", "message": "Command received"}
        client.publish(MQTT_TOPIC_RESPONSE.format(device_api_token=device_api_token), json.dumps(response_payload))

    except Exception as e:
        logger.error(f"Error processing message: {e}")

def start_mqtt_client():
    logger.info("Starting MQTT client...")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    try:
        mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        mqtt_client.tls_set()
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        logger.info(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
        mqtt_client.loop_start()
    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker: {e}")

# запуск MQTT клиента в отдельном потоке, чтобы не мешать Flask
logger.info("Starting MQTT thread...")
mqtt_thread = threading.Thread(target=start_mqtt_client, daemon=True)
mqtt_thread.start()

class Command(BaseModel):
    device_api_token: str
    cell_id: int = 0

@app.route('/send_command', methods=['POST'])
def send_command():
    try:
        data = request.get_json()
        command = Command(**data)

        if not mqtt_client.is_connected():
            logger.error("MQTT client is not connected. Attempting to reconnect...")
            mqtt_client.reconnect()

        topic = MQTT_TOPIC_COMMAND.format(device_api_token=command.device_api_token)
        command_payload = {"cell_id": command.cell_id}

        logger.info(f"Publishing message to topic {topic}")
        result = mqtt_client.publish(topic, json.dumps(command_payload))

        logger.info(f"Publish result: {result.rc}")  # (0 == success)
        if result.rc != 0:
            raise Exception(f"Failed to publish message, rc={result.rc}")

        return jsonify({"status": "success", "message": "Command sent successfully"}), 200

    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({"status": "error", "message": "Invalid data"}), 400
    except Exception as e:
        logger.error(f"Error during send_command: {e}")
        return jsonify({"status": "error", "message": "MQTT error occurred"}), 500
