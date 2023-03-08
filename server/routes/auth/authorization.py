from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import  status as response_status
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os
import dotenv
import pymongo
from dotenv import load_dotenv
import json

from server.database import database
from server.models.models import Basic_User, Token, TokenData, User_Client
from server.database_users_methods import get_user
from server.database_clients_methods import (
    add_client,
    
)
from server.database_users_methods import registration_checking
from server.routes.auth._router import auth_router as router
from server.auth_users_methods import ( verify_password, authenticate_user, create_access_token,
                                       get_current_user, get_current_active_user)
load_dotenv()

router = APIRouter(tags=['Authorization'])
ALGORITHM = os.getenv('ALGORITHM_FOR_AUTH')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

@router.post("/auth")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(database, 'Users_client', form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=user, expires_delta=access_token_expires
    )
    data_response = {
        'token': access_token,
        'user': user['login']
    }
    response = Response(json.dumps(data_response))
    response.set_cookie('Authorization', access_token)
    return (response)
    
@router.get("/auth/users/me/", response_model=Basic_User)
def read_users_me(current_user: Basic_User = Depends(get_current_active_user)):
    return current_user


@router.get("/auth/users/me/items/")
def read_own_items(current_user: Basic_User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user['login']}]


@router.post("/auth/registration",response_description="Client data added into the database", 
            status_code=response_status.HTTP_201_CREATED, )
def registration_client_user(request:Request, new_client:User_Client):
    try:        
        result_check = registration_checking(database, 'Users_client',new_client)
        if result_check:
            raise HTTPException(status_code=500, detail=f"A user with next fields: {result_check} already exists!", 
                                headers={"X-Error": "There goes my error"})
        new_client.password = new_client.hash_password(new_client.password)
        result = add_client(new_client)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data=dict(new_client), expires_delta=access_token_expires)
        response_data = {
            'token': access_token,
            'user': new_client.login,
        }
        response = Response (json.dumps(response_data))
        response.set_cookie('Authorization', access_token)
        return response
    except HTTPException as e:
        print (e.detail)
        raise HTTPException(status_code=500, detail=f"A user with next fields: {result_check} already exists!", 
                                headers={"X-Error": "There goes my error"})        


# @router.get("/auth/test/")
# async def auth_test(token):
#     user_frontend_info = jwt.decode(token, crypto_key, algorithms=[ALGORITHM])
#     return (user_frontend_info)
