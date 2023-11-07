import logging
import os

from mqtt.db import MqttMongoDbClient
from mqtt.mqtt import TTNMqttSaver
from mqtt import oracle_secrets


def start_mqtt_client(db_client):
    topic = os.environ.get("TTN_MQTT_TOPIC")
    api_key = oracle_secrets.retrieve_ttn_api_key()
    mqtt_client = TTNMqttSaver(os.environ.get("TTN_MQTT_USER"), api_key, db_client)
    mqtt_client.run(os.environ.get("TTN_MQTT_HOST"), int(os.environ.get("TTN_MQTT_PORT")), topic)
    return mqtt_client


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info("Starting MQTT Saver")
    with MqttMongoDbClient() as db_client:
        start_mqtt_client(db_client)
