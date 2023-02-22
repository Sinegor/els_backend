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

def registration_checking (db, collection, checking_user):
    """ checking unique fields at registration """
    result = db[collection].find_one({'$or':[{'login':checking_user.login}, {'userMail':checking_user.userMail}, 
            {'phoneNumber':checking_user.phoneNumber}]}, 
            projection={'login':True, 'userMail':True, 'phoneNumber':True, '_id':False})
    if not result:
        return True
    exist_data_fields = []
    [exist_data_fields.append(key) for key in result if result[key]== (dict(checking_user))[key]]
    return ', '.join(exist_data_fields)


def user_info(client) -> dict:
    return {
        "_id": str(client["_id"]),
        "login": client["login"],
        "userMail": client["userMail"],
        "phoneNumber": client["phoneNumber"],
        
    }

# Retrieve all clients present in the database
def get_users(db, collection):
    users = []
    for user in db[collection].find():
        users.append(json.loads(user))
    return users

# Retrieve a user with a matching ID
def get_user_by_id(db, collection, id: Union[str, ObjectId]) -> dict:
    user = db[collection].find_one({"_id": ObjectId(id)})
    return user

def get_user(db, collection, match:dict):
    user = db[collection].find_one(match)
    return user



