import os

from common.db import MongoDbClient

from data import Device, Message


class MqttMongoDbClient(MongoDbClient):
    def __init__(self):
        super().__init__()
        self._create_indexes()

    def _create_indexes(self):
        if "eui" not in self.get_device_collection().index_information():
            self.get_device_collection().create_index("eui")

    def save_device(self, device: Device):
        filter_query = {"eui": device.eui}
        device_data = device.__dict__
        self.get_device_collection().update_one(filter_query, {"$set": device_data}, upsert=True)

    def save_message(self, device: Device, message: Message):
        self.save_device(device)
        self.get_message_collection().insert_one(message)
