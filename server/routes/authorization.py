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

from server.database import database
from server.models.models import Basic_User, Token, TokenData, User_Client
from server.database_users_methods import get_user
from server.database_clients_methods import (
    add_client,
    
)
from server.database_users_methods import registration_checking

load_dotenv()

router = APIRouter(tags=['Authorization'])
crypto_key = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 120
crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")



def verify_password(checking_password, hashed_password) ->bool:
        return crypto_context.verify(checking_password, hashed_password)


def authenticate_user(db, collection, login: str, checking_password: str):
    searching_obj = {'login':login}
    user = get_user(db, collection, searching_obj)
    if not user:
        return False
    if not verify_password(checking_password, user['password']):
        return False
    user['_id'] = str(user['_id'])
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, crypto_key, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, crypto_key, algorithms=[ALGORITHM])
        print (payload)
        username: str = payload.get("login")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    searching_obj = {'login':token_data.username}
    user = get_user(database, 'Users_client', searching_obj)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: Basic_User = Depends(get_current_user)):
    if current_user['disabled']:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


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
    response = Response(access_token)
    
    response.set_cookie('Authorization', access_token)
    return (response)
    
    


@router.get("/auth/users/me/", response_model=Basic_User)
def read_users_me(current_user: Basic_User = Depends(get_current_active_user)):
    return current_user


@router.get("/auth/users/me/items/")
def read_own_items(current_user: Basic_User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user['login']}]


@router.post("/auth/registration",response_description="Client data added into the database", 
            status_code=response_status.HTTP_201_CREATED)
def registration_client_user(request:Request, new_client:User_Client):
    try:        
        result_check = registration_checking(database, 'Users_client',new_client)
        if not result_check:
            raise HTTPException(status_code=500, detail=f"A user with next fields: {result_check} already exists!", 
                                headers={"X-Error": "There goes my error"})
        new_client.password = new_client.hash_password(new_client.password)
        result = add_client(new_client)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(data=dict(new_client), expires_delta=access_token_expires)
    except HTTPException as e:
        print (e.detail)
        raise HTTPException(status_code=500, detail=f"A user with next fields: {result_check} already exists!", 
                                headers={"X-Error": "There goes my error"})        


@router.get("/auth/test/")
async def auth_test(token):
    user_frontend_info = jwt.decode(token, crypto_key, algorithms=[ALGORITHM])
    return (user_frontend_info)
