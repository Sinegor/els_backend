from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Union
from starlette.responses import JSONResponse
from pydantic import BaseModel
# Модуль для разрешения CORS-запросов
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from server.routes.clients.clients import router as Client_router
from server.routes.auth.authorization import router as Authorization_router
from server.database import my_mongo_client, clients_collection
from server.database_clients_methods import add_client
from server.consts import http


app = FastAPI(title='ILA')

# Список того, что разрешено передавать и какими методами пользоваться: 
app.add_middleware(
    CORSMiddleware,
    allow_origins = http.ELA_API_ORIGINS,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
    
    
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to this fantastic app!"}




app.include_router(Client_router)
app.include_router(Authorization_router)

if __name__ == "__main__":
    import logging
    import uvicorn
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('unicorn')
    logger.setLevel(logging.DEBUG)

    uvicorn.run(app, host ="127.0.0.1", port=8000)






