from typing import Optional, Union, Sequence

import pymongo
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError


class MongoDbClient:
    def __init__(self, host: Optional[Union[str, Sequence[str]]]="mongodb://localhost:27017",
                 db_name: str = "mqtt_database",
                 connection_timeout: int = 7500):
        self.host = host
        self.db_name = db_name
        self.connection_timeout = connection_timeout

        self.client: Optional[MongoClient] = None
        self.database: Optional[Database] = None

    def start(self):
        try:
            self.client = pymongo.MongoClient(self.host,
                                              serverSelectionTimeoutMS=self.connection_timeout)
            self.database = self.client[self.db_name]
            self.client.server_info()  # Do some request to check connection
            return self
        except ServerSelectionTimeoutError as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()
