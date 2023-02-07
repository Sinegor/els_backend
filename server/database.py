import motor.motor_asyncio
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId


MONGO_DETAILS = "mongodb://localhost:27017"

my_mongo_client = AsyncIOMotorClient(MONGO_DETAILS)
my_mongo_client.get_io_loop = asyncio.get_running_loop

database = my_mongo_client.ELS

lawyers_collection = database.get_collection("Users_lawyers")
clients_collection = database.get_collection("Users_client")
legal_application_collection = database.get_collection("Legal_aid_application")
authorization_collection = database.get_collection("Authorization_data")
