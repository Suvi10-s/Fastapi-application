from pydantic import BaseModel,EmailStr, Field
from typing import Optional

class User_details(BaseModel):
    username: str
    email:EmailStr
    password: str

class GetUser(BaseModel):
    username: str
    email:EmailStr

class add_user(BaseModel):
    username:str
    password:str
    email:EmailStr

class updating_user(BaseModel):
    newusername:Optional[str]
    newpassword:Optional[str]