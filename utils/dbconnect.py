from pymongo import MongoClient

# connect_string = f'mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DBNAME}?authSource=admin'
# client = MongoClient(connect_string)

def connect():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.library
    return db
# collection = db['customers']
