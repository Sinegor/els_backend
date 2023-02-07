from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database_clients_methods import (
    add_client,
    delete_client,
    retrieve_clients,
    retrieve_client,
    update_client,
)
from server.models.models import (
    ErrorResponseModel,
    ResponseModel,
    Client_Registration_Schema,
    Registration_Client_Data
    #UpdateStudentModel,
)

router = APIRouter(prefix="/client", tags=["Client"])

@router.post("/registration", response_model=Registration_Client_Data, response_description="Client data added into the database")
async def add_client_data(data: Client_Registration_Schema):
    print ('I am here!')
    client = jsonable_encoder(data)
    new_client = await add_client(data)
    return ResponseModel(new_client, "Client added successfully.")

