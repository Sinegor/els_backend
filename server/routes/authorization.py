from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from server.database import database
import os
import dotenv
from server.models.models import Basic_User, Token, TokenData
from server.database_users_methods import get_user
from dotenv import load_dotenv
import pymongo

load_dotenv()

router = APIRouter(prefix="/authorization", tags=['Authorization'])
crypto_key = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120
crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token", response_model=Token)
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
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=Basic_User)
async def read_users_me(current_user: Basic_User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: Basic_User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

