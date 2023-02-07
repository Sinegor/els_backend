import motor
import motor.motor_asyncio
from bson import ObjectId

from server.database import (MONGO_DETAILS, my_mongo_client, database,  
                     lawyers_collection, clients_collection,)
                    

def client_info(client) -> dict:
    return {
        "id": str(client["_id"]),
        "login": client["login"],
        "userMail": client["userMail"],
        "phoneNumber": client["phoneNumber"],
        "legal_help_applications": client["legal_help_applications"]
        
    }

# Retrieve all clients present in the database
async def retrieve_clients():
    clients = []
    async for client in clients_collection.find():
        clients.append(client_info(client))
    return clients

# Retrieve a client with a matching ID
async def retrieve_client(id: str) -> dict:
    client = await clients_collection.find_one({"_id": ObjectId(id)})
    if client:
        return client_info(client)

# Add a new client into to the database
async def add_client(client_data: dict) -> dict:
    client = await clients_collection.insert_one(client_data)
    new_client = await clients_collection.find_one({"_id": client.inserted_id})
    return client_info(new_client)

# Update a client with a matching ID
async def update_client(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    client = await clients_collection.find_one({"_id": ObjectId(id)})
    if client:
        updated_client = await clients_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_client:
            return True
        return False
    return False # необходимо прописать ошибку отсутствия такого клиента.

# Delete a client from the database
async def delete_client(id: str):
    client = await clients_collection.find_one({"_id": ObjectId(id)})
    if client:
        await clients_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False # необходимо прописать ошибку отсутствия такого клиента.