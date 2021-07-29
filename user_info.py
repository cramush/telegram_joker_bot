import pymongo
import config

client = pymongo.MongoClient(f"mongodb://{config.login}:{config.password}@{config.host}/{config.db_name}")
db = client["users_info_db"]
info_collection = db["info"]
if info_collection.estimated_document_count() == 0:
    info_collection.drop()
    info_collection.create_index([("username", pymongo.ASCENDING), ("date", pymongo.ASCENDING)])


def user_info(message):
    info_from = message["from"]

    info_id = info_from["id"]
    info_first_name = info_from["first_name"]
    info_username = info_from["username"]
    info_date = message["date"]
    info_text = message["text"]

    user_info_container = {
        "user_id": info_id,
        "first_name": info_first_name,
        "username": info_username,
        "date": info_date,
        "content": info_text
    }

    info_collection.insert_one(user_info_container)
