import pymongo


class MongoDbClient:
    def __init__(self, host="mongodb://localhost:27017", db_name="mqtt_database",
                 connection_timeout=7500):
        self.host = host
        self.db_name = db_name
        self.connection_timeout = connection_timeout

        self.client = None
        self.database = None

    def start(self):
        try:
            self.client = pymongo.MongoClient(self.host,
                                              serverSelectionTimeoutMS=self.connection_timeout)
            self.database = self.client[self.db_name]
            self.client.server_info()  # Do some request to check connection
            return self
        except pymongo.errors.ServerSelectionTimeoutError as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()
