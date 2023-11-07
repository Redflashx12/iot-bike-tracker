import json
import logging
import re

import certifi
import paho.mqtt.client as mqtt


class TTNMqttSaver(mqtt.Client):
    def __init__(self, username, api_key, db_client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username_pw_set(username=username, password=api_key)
        self.tls_set(certifi.where())
        self.enable_logger()

        self.db_client = db_client

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT broker")
        else:
            logging.error(f"Failed to connect with result code {rc}")

    @staticmethod
    def _extract_device_id_from_topic(topic):
        device_id_search = re.search(r".*/devices/(.*)/.*", topic)
        return device_id_search.group(1)

    @staticmethod
    def _create_object_from_message(message):
        payload = json.loads(message.payload)
        uplink_msg = payload.get("uplink_message", {})
        message_data = {
            "device_id": TTNMqttSaver._extract_device_id_from_topic(message.topic),
            "count": uplink_msg.get("f_cnt", None),
            "payload": uplink_msg.get("frm_payload", None),
            "rx_metadata": uplink_msg.get("rx_metadata", {}),
            "consumed_airtime": uplink_msg.get("consumed_airtime", None),
            "decoded_payload": uplink_msg.get("decoded_payload", {})
        }
        return message_data

    def on_message(self, client, userdata, message):
        try:
            received_data = self._create_object_from_message(message)
            device_id = received_data["device_id"]
            logging.info(f"New message received from {device_id}")
            self.db_client.save_message(device_id, received_data)
        except Exception:
            logging.exception("Skipping message due to exception")

    def run(self, host, port, topics):
        self.connect(host, port)
        self.subscribe(topics)
        self.loop_forever()

    def run_non_blocking(self, host, port, topics):
        self.connect_async(host, port)
        self.subscribe(topics)
        self.loop_start()
