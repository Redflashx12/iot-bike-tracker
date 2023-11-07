from common.db import MongoDbClient


class MqttMongoDbClient(MongoDbClient):
    def __init__(self):
        super().__init__()

    def _get_device_collection(self, device_id):
        if device_id in self.database.list_collection_names():
            return self.database[device_id]
        else:
            return self.database.create_collection(device_id)

    def save_message(self, device_id, message):
        device_collection = self._get_device_collection(device_id)
        device_collection.insert_one(message)
