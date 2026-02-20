from pydantic import BaseModel,EmailStr

class User_details(BaseModel):
    username: str
    email:EmailStr
    password: str

class Get_user(BaseModel):
    username: str
    email:EmailStr
    message:str

class Login_info(BaseModel):
    username:str
    password:str