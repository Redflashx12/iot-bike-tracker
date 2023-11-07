from api.api import create_app
from api.db import ApiMongoDbClient

if __name__ == '__main__':
    with ApiMongoDbClient() as db_client:
        app = create_app(db_client)
        app.run()
else:
    # Gunicorn
    db_client = ApiMongoDbClient()
    db_client.start()
    app = create_app(db_client)
