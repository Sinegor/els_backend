from bson import ObjectId
import pymongo
from server.database import (my_mongo_client, database,  
                     lawyers_collection, clients_collection,)
from server.models.models import User_Client_Registration_Schema, User_Client
from jose import JWTError, jwt
from passlib.context import CryptContext
import json
import typing
from typing import Union

crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                    
# Add a new client into to the database
def add_client(client_data: User_Client):
    new_client = clients_collection.insert_one(client_data.dict())
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




