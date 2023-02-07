from typing import Union, List, Any, Dict, Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from starlette.exceptions import HTTPException as StarletteHTTPException


class Registration_Client_Data (BaseModel):
    login: str = Field(...)
    userMail:str = Field(...)
    password: str = Field(...)
    phoneNumber: str = Field (...)
    legal_help_applications: Union[None, List]
    payment_details: Union[None, str]

class Client_Registration_Schema(BaseModel):
    login: str = Field(...)
    userMail: EmailStr = Field(...)
    password: str = Field(...)
    phoneNumber: str 
    legal_help_applications: Union[None, List]
    payment_details: Union[None, str]
    class Config:
        schema_extra = {
            "example": {
                'login': "Avatar",
                'userMail': "ggg@gmail.com",
                'password': '1111111111111',
                'phoneNumber': '+72121121212' 
            }
        }



class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise TypeError('ObjectId required')
        return str(v)

    
## Схема, которая показывается на docs#:
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "fullname": "John Doe",
    #             "email": "jdoe@x.edu.ng",
    #             "course_of_study": "Water resources engineering",
    #             "year": 2,
    #             "gpa": "3.0",
    #         }
    #     }
    

class Client_applicant (Registration_Client_Data):
      needs_help_name: str
      nedds_help_surname: str

class Registration_Lawyer_Data(BaseModel):
    login:  str
    name: str
    surname:  str  #возможно эти поля можно объеденить
    advokat:   bool
    email:  str
    phoneNumber: str
    preferred_location: dict # Объект с двумя ключами: территориальный район и госуларственные органы. 
    # Каждому ключу соответствует массив значений, длина массива фиксированная (например не больше 3) 
    specialization: List # фиксированный по длине список значений для конкретного юриста, 
    # второй вариант - словарь, в котором в качестве свойств указываются все предлагаемые при регистрации
    # специализации, а их значением выступают true/false
    incompetence: List #аналогично предыдущему пункту
    current_applications: Union[None, List[PydanticObjectId]]
    completed_applications: Union[None, List[PydanticObjectId]]
    status: Union[None, str] #"is availible/is not available/is working",
    geolocation: None
    rating: None # объект, над свойствами надо подумать



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

# class HTTPException(StarletteHTTPException):
#     def __init__(
#         self,
#         status_code: int,
#         detail: Any = None,
#         headers: Optional[Dict[str, Any]] = None,
#     ) -> None:
#         super().__init__(status_code=status_code, detail=detail)
#         self.headers = headers


# Information is taken from the site. It is not clear why the functions and not classes:
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}

