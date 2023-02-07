import motor.motor_asyncio
from bson import ObjectId


MONGO_DETAILS = "mongodb://localhost:27017"

my_mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = my_mongo_client.ELS

lawyers_collection = database.get_collection("Users_lawyers")
clients_collection = database.get_collection("Users_client")
legal_application_collection = database.get_collection("Legal_aid_application")
authorization_collection = database.get_collection("Authorization_data")
