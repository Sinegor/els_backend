import motor.motor_asyncio
from bson.objectid import ObjectId
import database
from database import (MONGO_DETAILS, my_mongo_client, database,  
                     lawyers_collection, clients_collection, legal_application_collection,
                     authorization_collection)

def legal_application_info(app) ->dict:
    return{
        "id": str(app["_id"]),
        "id_client": str (app["id_client"]),
        "specialization": app["specialization"],
        "status": app["status"],
        "id_lawyer": str(app["id_lawyer"])
    }

# Retrieve all applications present in the database
async def retrieve_applications():
    applications = []
    async for application in legal_application_collection.find():
        applications.append(legal_application_info(application))
    return applications


# Add a new application into to the database
async def add_application(application_data: dict) -> dict:
    application = await legal_application_collection.insert_one(application_data)
    new_application = await legal_application_collection.find_one({"_id": application.inserted_id})
    return legal_application_info(new_application)


# Retrieve a application with a matching ID
async def retrieve_application(id: str) -> dict:
    application = await legal_application_collection.find_one({"_id": ObjectId(id)})
    if application:
        return legal_application_info(application)
    return False #необходимо прописать ошибку отсутствия


# Update a application with a matching ID
async def update_application(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    application = await legal_application_collection.find_one({"_id": ObjectId(id)})
    if application:
        updated_application = await legal_application_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_application:
            return True
        return False
    return False #необходимо прописать ошибку отсутствия


# Delete a application from the database
async def delete_application(id: str):
    application = await legal_application_collection.find_one({"_id": ObjectId(id)})
    if application:
        await legal_application_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False #необходимо прописать ошибку отсутствия