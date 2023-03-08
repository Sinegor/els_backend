from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, HTTPException, status 
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os
import dotenv

from dotenv import load_dotenv
import json

from server.models.models import Basic_User, Token, TokenData, User_Client
from server.database_users_methods import get_user
from server.database_clients_methods import (
    add_client,
    
)
from server.database_users_methods import registration_checking
from server.routes.auth._router import auth_router as router
from server.database import database
from server.dependencies import oauth2_scheme

load_dotenv()
crypto_key = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"


def verify_password(checking_password, hashed_password) ->bool:
        crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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
