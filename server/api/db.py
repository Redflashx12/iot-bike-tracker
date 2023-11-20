import pymongo
from ..common.db import MongoDbClient


class ApiMongoDbClient(MongoDbClient):
    def __init__(self):
        super().__init__()

    def get_all_device_ids(self):
        return self.database.list_collection_names()

    def get_messages_of_device(self, device_id: str, page_num: int, page_size: int,
                               from_dt: str, to_dt: str):
        device_collection = self.database[device_id]
        total_messages = device_collection.count_documents({})

        query = {"rx_metadata.0.received_at": {"$gte": from_dt, "$lt": to_dt}}
        messages = list(device_collection.find(query)
                        .skip((page_num - 1) * page_size)
                        .limit(page_size)
                        .sort('count', pymongo.DESCENDING)
                        )
        return messages, total_messages
