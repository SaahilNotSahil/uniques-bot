import os
from urllib.parse import quote_plus

import mongoengine
from dotenv import load_dotenv

from utils import logger


def connect():
    load_dotenv()

    username = quote_plus(str(os.getenv('MONGODB_USERNAME')))
    password = quote_plus(str(os.getenv('MONGODB_PASSWORD')))
    host = quote_plus(str(os.getenv("MONGODB_HOST")))

    uri = f"mongodb+srv://{username}:{password}@{host}/"
    uri += "?retryWrites=true&w=majority"

    try:
        mongoengine.register_connection(alias="default", name="uniques")
        mongoengine.connect(host=uri)
    except mongoengine.connection.ConnectionFailure:
        logger.error("MongoDB connection failed")

        return

    logger.info("MongoDB connection successful")
