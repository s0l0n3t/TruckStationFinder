from pymongo import MongoClient



url = "mongodb://localhost:27017/"
client = MongoClient("localhost",27017)

db = client.trackstation
