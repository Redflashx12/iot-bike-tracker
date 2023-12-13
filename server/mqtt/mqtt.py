import json
import logging

import certifi
import paho.mqtt.client as mqtt

from data import Device, Message


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
    def _create_device_from_message(message) -> Device:
        try:
            device_ids = message["end_device_ids"]
            eui = device_ids["dev_eui"]
            ttn_id = device_ids["device_id"]
            return Device(eui, ttn_id)
        except KeyError as e:
            raise InvalidMqttMessageError("MQTT message payload didn't contain all necessary data "
                                          "in the 'end_device_ids' field.") from e

    @staticmethod
    def _create_message(json_message, device) -> Message:
        try:
            uplink_msg = json_message["uplink_message"]
            count = uplink_msg["f_cnt"]
            payload = uplink_msg["frm_payload"]
            decoded_payload = uplink_msg["decoded_payload"]
            rx_metadata = uplink_msg["rx_metadata"]
            consumed_airtime = uplink_msg["consumed_airtime"]
            return Message(device.eui, count, payload, decoded_payload, rx_metadata,
                           consumed_airtime)
        except KeyError as e:
            raise InvalidMqttMessageError("MQTT message payload didn't contain all necessary data "
                                          "in the 'uplink_message' field.") from e

    @staticmethod
    def _create_data_from_mqtt_message(mqtt_message):
        json_message = json.loads(mqtt_message.payload)
        device = TTNMqttSaver._create_device_from_message(json_message)
        message = TTNMqttSaver._create_message(json_message, device)
        return device, message

    def on_message(self, client, userdata, message):
        try:
            device, message = self._create_data_from_mqtt_message(message)
            logging.info(f"New message received from {device.ttn_id}")
            self.db_client.save_message(device, message)
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


class InvalidMqttMessageError(Exception):
    pass
