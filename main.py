from fastapi import FastAPI
from crud import crud
from services import router


app= FastAPI(title='user registration and login')
app.include_router(router,prefix='/api',tags=['user'])
app.include_router(crud,prefix='/crud',tags=['crud operations'])

# def hash_password(username:str,password:str):
#     password_bytes=password.encode()
#     salt=bcrypt.gensalt()
#     hashed_password=bcrypt.hashpw(password_bytes,salt)
#     return hashed_password
# def check_password(password:str,hashed:str):
#     checked_password=bcrypt.checkpw(password.encode(),hashed)
#     return checked_password
