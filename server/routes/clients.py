from fastapi import APIRouter, Body, Request
#from fastapi.encoders import jsonable_encoder
from fastapi import Depends, status as response_status, HTTPException, Request, Response
from server.database_clients_methods import (
    add_client,
    delete_client,
    retrieve_clients,
    retrieve_client,
    update_client,
)
from server.models.models import (
    ErrorResponseModel,
    User_Client_Registration_Schema, User_Client
)

router = APIRouter(prefix="/client", tags=["Client"])

@router.post("/registration",response_description="Client data added into the database", 
            status_code=response_status.HTTP_201_CREATED)

def registration_client_user(request:Request, new_client:User_Client)->str:  
        result = add_client(new_client)
        return str(result.inserted_id)
