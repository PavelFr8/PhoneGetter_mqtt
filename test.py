import os
import logging
from dotenv import load_dotenv
from paho.mqtt.client import Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
MQTT_BROKER = os.environ.get("MQTT_BROKER")
MQTT_PORT = int(os.environ.get("MQTT_PORT"))
MQTT_USERNAME = os.environ.get("MQTT_USERNAME")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
MQTT_TOPIC = "device/123/command"

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        logger.info(f"Received message: Topic={msg.topic}, Payload={payload}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

def start_subscriber():
    client = Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.tls_set()
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.subscribe(MQTT_TOPIC)
        logger.info(f"Subscribed to topic: {MQTT_TOPIC}")
        client.loop_forever()
    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker: {e}")

if __name__ == "__main__":
    start_subscriber()
