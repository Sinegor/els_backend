from fastapi import FastAPI
from typing import Union
from starlette.responses import JSONResponse
from pydantic import BaseModel
from .models.models import Registration_Client_Data, Registration_Lawyer_Data
# Модуль для разрешения CORS-запросов
from fastapi.middleware.cors import CORSMiddleware
from server.routes.clients import router as Client_router
from server.database import my_mongo_client, clients_collection
from server.database_clients_methods import add_client


#Data for first testing test
# testing_logins =[]

# testing_client_data = {
    

# }

# получаем экземпляр главного класса Fastapi, которорый в свою очередь наследуется от Starlette.
# Данный экземпляр, соответственно, обладает всеми необходимыми свойствами и методами:

app = FastAPI()
app.include_router(Client_router)
# Список разрешённых адресов для CORS-запросов:
origins = [
    "http://localhost",
    'http://localhost:3000',
    "http://localhost:8080",
]
# Список того, что разрешено передавать и какими методами пользоваться:
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}





# @app.post(f"/registration/client/",)
# def create_client(data):
#     return add_client(data)





## Testing route:
# def make_registration_client(data:Registration_Client_Data):
#     try:
#         if data.login in testing_logins:
#             return print('Клиент с таким именем уже существует')
#         testing_client_data[data.login]={
#             'password':data.password,
#             'userMail':data.userMail,
#             'phoneNumber':data.phoneNumber
#         }
#         testing_logins.append(data.login)
#         print ('Вы успешно зарегистрировались')
#         return testing_client_data
    
#     except Exception as e:
#         print(e)


