from common.db import MongoDbClient


class ApiMongoDbClient(MongoDbClient):
    def __init__(self):
        super().__init__()

    def get_all_device_ids(self):
        return self.database.list_collection_names()

    def get_messages(self, device_id, page_num, page_size):
        device_collection = self.database[device_id]
        messages = list(device_collection.find().skip((page_num - 1) * page_size).limit(page_size))
        return messages
