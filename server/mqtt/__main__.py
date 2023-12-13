import logging
import os

from mqtt.db import MqttMongoDbClient
from mqtt.mqtt import TTNMqttSaver
from mqtt import oracle_secrets


def start_mqtt_client(db_client):
    api_key = oracle_secrets.retrieve_ttn_api_key()
    mqtt_client = TTNMqttSaver(os.environ.get("ttn.mqtt.user"), api_key, db_client)
    host = os.environ.get("ttn.mqtt.host")
    port = int(os.environ.get("ttn.mqtt.port"))
    topic = os.environ.get("ttn.mqtt.topic")
    mqtt_client.run(host, port, topic)
    return mqtt_client


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info("Starting MQTT Saver")
    device_collection = os.environ.get("db.device_collection")
    msg_collection = os.environ.get("db.message_collection")
    with MqttMongoDbClient(device_collection_name=device_collection,
                           message_collection_name=msg_collection) as db_client:
        start_mqtt_client(db_client)
