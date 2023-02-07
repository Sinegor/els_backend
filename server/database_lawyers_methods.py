import motor.motor_asyncio
from bson.objectid import ObjectId
import database
from database import (MONGO_DETAILS, my_mongo_client, database,  
                     lawyers_collection, clients_collection, legal_application_collection,
                     authorization_collection)
def lawyer_info(lawyer) -> dict:
    return{
        "id": str(lawyer["_id"]),
        "login": lawyer["login"],
        "email": lawyer["email"],
        "phoneNumber": lawyer["phoneNumber"],
        "name": lawyer["name"],
        "surname": lawyer["surname"],
        "preferred_location": lawyer["preferred_location"],
        "specialization": lawyer["specialization"],
        "status": lawyer["status"],
        "rating": lawyer["rating"]
    }

# Retrieve all lawyers present in the database
async def retrieve_lawyers():
    lawyers = []
    async for lawyer in lawyers_collection.find():
        lawyers.append(lawyer_info(lawyer))
    return lawyers


# Add a new lawyer into to the database
async def add_lawyer(lawyer_data: dict) -> dict:
    lawyer = await lawyers_collection.insert_one(lawyer_data)
    new_lawyer = await lawyers_collection.find_one({"_id": lawyer.inserted_id})
    return lawyer_info(new_lawyer)


# Retrieve a lawyer with a matching ID
async def retrieve_lawyer(id: str) -> dict:
    lawyer = await lawyers_collection.find_one({"_id": ObjectId(id)})
    if lawyer:
        return lawyer_info(lawyer)
    return False # необходимо прописать ошибку


# Update a lawyer with a matching ID
async def update_lawyer(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    lawyer = await lawyers_collection.find_one({"_id": ObjectId(id)})
    if lawyer:
        updated_lawyer = await lawyers_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_lawyer:
            return True
        return False
    return False # необходимо прописать ошибку


# Delete a lawyer from the database
async def delete_lawyer(id: str):
    lawyer = await lawyers_collection.find_one({"_id": ObjectId(id)})
    if lawyer:
        await lawyers_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False # необходимо прописать ошибку