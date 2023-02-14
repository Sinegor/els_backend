from fastapi import APIRouter, Body, Request, HTTPException, Response, Depends
#from fastapi.encoders import jsonable_encoder
from fastapi import  status as response_status
import pydantic
from server.database_clients_methods import (
    add_client,
    
)
from server.database_users_methods import registration_checking
from server.models.models import (
    ErrorResponseModel,
    User_Client_Registration_Schema, User_Client
)
from server.database import my_mongo_client, database, clients_collection
router = APIRouter(prefix="/client", tags=["Client"])
import pymongo
    
@router.post("/registration",response_description="Client data added into the database", 
            status_code=response_status.HTTP_201_CREATED)
def registration_client_user(request:Request, new_client:User_Client):
    try:        
        result_check = registration_checking(database, 'Users_client',new_client)
        if result_check:
            raise HTTPException(status_code=500, detail=f"A user with next fields: {result_check} already exists!", 
                                headers={"X-Error": "There goes my error"})
        new_client.password = new_client.hash_password(new_client.password)
        result = add_client(new_client)
        return str(result.inserted_id)
    except HTTPException as e:
        print (e.detail)
        raise HTTPException(status_code=500)
        
        