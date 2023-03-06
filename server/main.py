from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

from typing import Union
from starlette.responses import JSONResponse
from pydantic import BaseModel
# Модуль для разрешения CORS-запросов
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from server.routes.clients import router as Client_router
from server.routes.authorization import router as Authorization_router
from server.database import my_mongo_client, clients_collection
from server.database_clients_methods import add_client


#Data for first testing test
# testing_logins =[]

# testing_client_data = {
    

# }

# получаем экземпляр главного класса Fastapi, которорый в свою очередь наследуется от Starlette.
# Данный экземпляр, соответственно, обладает всеми необходимыми свойствами и методами:

app = FastAPI()
# Список разрешённых адресов для CORS-запросов:
origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:3000",
    "https://localhost:3000",
 ]
# practic of auth:


# Список того, что разрешено передавать и какими методами пользоваться:
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
    
    
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to this fantastic app!"}




app.include_router(Client_router)
app.include_router(Authorization_router)






