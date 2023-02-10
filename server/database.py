#import motor.motor_asyncio
#import asyncio
#from motor.motor_asyncio import AsyncIOMotorClient
import pymongo
import os
from dotenv import load_dotenv
from bson import ObjectId
from pymongo import MongoClient
load_dotenv()
mongo_url = os.getenv("ETL_MONGO_DB_URL")
#async solution:
#my_mongo_client = AsyncIOMotorClient(MONGO_DETAILS)
#my_mongo_client.get_io_loop = asyncio.get_running_loop

my_mongo_client = MongoClient(mongo_url)
database = my_mongo_client.ELS
lawyers_collection = database.get_collection("Users_lawyers")
clients_collection = database.get_collection("Users_client")
legal_application_collection = database.get_collection("Legal_aid_application")
authorization_collection = database.get_collection("Authorization_data")
