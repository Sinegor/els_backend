from typing import Union, List, Any, Dict, Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from starlette.exceptions import HTTPException as StarletteHTTPException
from passlib.context import CryptContext
import os
crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise TypeError('ObjectId required')
        return str(v)

class UserDetails(BaseModel):
    roles: Optional[List[str]] # need to think about, for example client andl lawyer, may be also role in application or rating
    meta: Optional[Dict[str, str]]  # need to think about, may be it is not neсessary

class Basic_User (BaseModel):
    login: str = Field(...)
    userMail:EmailStr = Field(...)
    email_verified: Optional[bool]
    password: Union[str, bytes] = Field(...)
    phoneNumber: str = Field (...)
    details: Optional[UserDetails]
    disabled: Union[bool, None]
    last_activity: Optional[str] # need to change "str" for another type
    last_modification: Optional[str] # need to change "str" for another type
    modified_by: Optional[str] # need to think about, may be it is not neсessary
    
    def hash_password(self,password:str):
        return crypto_context.hash(password)
    
    def is_admin(self)-> bool:
        pass
                        # check user ащк фвьшт ыефегы
    def get_location(self) -> Dict: # need to think about type
        pass

    def create_disput(self):
        pass


class User_Client (Basic_User):
    payment_details: Union[None, Dict]
    legal_help_applications: Union[None, List]
    def set_payment_method(self):
        pass 
    def make_the_payment(self):
        pass

    def create_app_for_legal_aid(self):
        pass
    
    def confirm_arrival_lawyer (self):
        pass
    def end_contract(self):
        pass
    
    def confirm_contract(self):
        pass

class User_Client_Registration_Schema(BaseModel):
    login: str = Field(...)
    userMail: EmailStr = Field(...)
    password: str = Field(...)
    phoneNumber: str 
    class Config:
        schema_extra = {
            "example": {
                'login': "Avatar",
                'userMail': "ggg@gmail.com",
                'password': '1111111111111',
                'phoneNumber': '+72121121212' 
            }
        }

class User_Lawyer(Basic_User):
    name: str = Field(...)
    surname:  str = Field(...)  #возможно эти поля можно объеденить
    advokat:   bool
    legal_edecation_check: Optional[bool]
    advokat_status_check: Optional[bool]
    preferred_location: Dict # obj with two keys: location and state institutions, values is 
    #lists with fix length (3 for example)
    specialization: List = Field(...) #  list with fix length or dict
    incompetence: List= Field(...) # similarly above
    current_applications: Union[None, List[PydanticObjectId]]
    completed_applications: Union[None, List[PydanticObjectId]]
    status: Union[None, str] #"is availible/is not available/is working",
    current_location: Optional[str] # may be another type, not "str"
    
    def check_status(self)->str:  #regular status request, may be it is a class method
        pass 

    def accept_application(self):
        pass

    def request_confirmation_arrival (self):
        pass
    
    def conclude_contract (self):
        pass
    
class User_Lawyer_Registration_Schema(BaseModel):
    login: str = Field(...)
    userMail: EmailStr = Field(...)
    password: str = Field(...)
    phoneNumber: str  = Field(...)
    name: str= Field(...)
    surname:  str = Field(...)
    advokat:   bool= Field(...)
    preferred_location: Dict 
    specialization: List = Field(...) 
    incompetence: List= Field(...) 
    class Config:
        schema_extra = {
            "example": {
                'login': "Mr Smitt",
                'userMail': "ggg@gmail.com",
                'password': '66666666666',
                'phoneNumber': '+72121121212', 
                'name': 'Ivan',
                'surname': 'Ivanov',
                'advokat': False,
                'preferred_location':{
                    'place': 'Muhosransky district',
                    'state institutions': 'Police of Muhosransk',
                },
                'specialization': ['civil law'],
                'incompetence': ['public law']
            }
        }


class Legal_aid_application(BaseModel):
     id_client: PydanticObjectId
     type: str # указывается один из трёх вариантов работы приложения
     date: str
     place: dict #  объект со свойствами: геолокация (значение могут быть координаты или false ), 
     #готов приехать к юристу (значение true/false), орган власти(значение или название органа или false)*/
     specialization: List #список совпадает с предлагаемым юристам при регистрации//
     status: str #(поиск исполнителя, в процессе выполнения, окончена, диспут) 
     id_lawyer: Union[None, PydanticObjectId]            
    

class Authorization_data(BaseModel):
    id: PydanticObjectId # ObjectId из соответствующей коллекции (юрист или заказчик)
    password: str
    type: str # юрист или заказчик
    is_admin: bool


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

