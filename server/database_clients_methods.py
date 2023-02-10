import motor
import motor.motor_asyncio
from bson import ObjectId

from server.database import (my_mongo_client, database,  
                     lawyers_collection, clients_collection,)
from server.models.models import User_Client_Registration_Schema, User_Client
                    

def client_info(client) -> dict:
    return {
        "_id": str(client["_id"]),
        "login": client["login"],
        "userMail": client["userMail"],
        "phoneNumber": client["phoneNumber"],
        "legal_help_applications": client["legal_help_applications"]
        
    }

# Retrieve all clients present in the database
def retrieve_clients():
    clients = []
    for client in clients_collection.find():
        clients.append(client_info(client))
    return clients

# Retrieve a client with a matching ID
def retrieve_client(id: str) -> dict:
    client = clients_collection.find_one({"_id": ObjectId(id)})
    if client:
        return client_info(client)

# Add a new client into to the database
def add_client(client_data: User_Client):
    new_client = clients_collection.insert_one(client_data.dict())
    #new_client = clients_collection.find_one({"_id": client.inserted_id})
    return (new_client)

# Update a client with a matching ID
def update_client(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    client = clients_collection.find_one({"_id": ObjectId(id)})
    if client:
        updated_client = clients_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_client:
            return True
        return False
    return False # необходимо прописать ошибку отсутствия такого клиента.

# Delete a client from the database
def delete_client(id: str):
    client = clients_collection.find_one({"_id": ObjectId(id)})
    if client:
        clients_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False # необходимо прописать ошибку отсутствия такого клиента.