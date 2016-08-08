import json
from pymongo import MongoClient

def insert_data(data, db):
    for row in data:
        db.larochelle.insert(row)

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017")
    db = client.larochelle

    with open('files/processed-la-rochelle_france.json') as f:
        data = json.loads(f.read())
        insert_data(data, db)
        print db.larochelle.find_one()
