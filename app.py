from fastapi import FastAPI,HTTPException,Depends
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from datetime import datetime,timedelta
from jose import jwt,JWTError
import bcrypt
from models import User_details,Get_user,Login_info
app= FastAPI(title='user registration and login')

# @app.get("/contact")
# def say_about(name:str,contact:int):
#     return {'name':name,'contact':contact}

# def hash_password(username:str,password:str):
#     password_bytes=password.encode()
#     salt=bcrypt.gensalt()
#     hashed_password=bcrypt.hashpw(password_bytes,salt)
#     return hashed_password
# def check_password(password:str,hashed:str):
#     checked_password=bcrypt.checkpw(password.encode(),hashed)
#     return checked_password
user_db={}
ALGORITHM='HS256'
SECRET_KEY='suvi123'
security=HTTPBearer()

@app.post('/register')
def user_registration(user:User_details):
    if user.username in user_db:
        raise HTTPException(status_code=400,detail='user alreaady exist')
    hashed_password=bcrypt.hashpw(user.password.encode(),bcrypt.gensalt())
    user_db[user.username]={'username':user.username,'email':user.email,
                       'password':hashed_password}
    return {'user':'successfully registered'}

@app.get('/user-details',response_model=Get_user)
def get_user(username:str):
    if username not in user_db:
        raise HTTPException(status_code=404,detail='User not found')
    return {'username':username,'email':user_db[username]['email'],'message':'displaying user successfully'}


@app.post('/login')
def login(user:User_details):
    if user.username not in user_db:
        raise HTTPException(status_code=404,detail='username not found' )
    stored_password = user_db[user.username]["password"]
    if not bcrypt.checkpw(user.password.encode(),stored_password):
        raise HTTPException(status_code=401,detail='invalid password')
    payload={'user':user.username,
             'email':user.email,
             'exp':datetime.utcnow()+timedelta(minutes=30)}
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return{'access token':token}

# @app.get('/verify_token')
# def verify_token(credentials:HTTPAuthorizationCredentials=Depends(security)):
#     token=credentials.credentials
#     if token in blacklisted:
#         raise HTTPException(status_code=401,detail='token logged out')
#     try:
#         payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
#         return payload
#     except JWTError:
#         raise HTTPException(status_code=403,detail='invalid or expired token')
    
# @app.get('/list')
# def list_user(users=Depends(verify_token)):
#     return {'logged user': users['user'],'all_list':list(user_db.keys())}

# @app.delete('/delete')
# def delete_user(current_user:dict=Depends(verify_token)):
#     username=current_user['user']
#     if username not in user_db:
#         raise HTTPException(status_code=404,detail='user not found')
#     del user_db[username]
#     return {'status':'success','deleted_user':username}

# @app.post('/add_user')
# def add_user(username:str,password:str,user:dict=Depends(verify_token)):
#     if username in user_db:
#         raise HTTPException(status_code=400,detail='user already exists')
#     hashed_password=bcrypt.hashpw(password.encode(),bcrypt.gensalt())
#     user_db[username]={'username':username,
#                        'password':hashed_password}
#     return {'message':f'user {username} added successfully'}
# blacklisted=set()

# @app.post('/logout')
# def logout(credentials:HTTPAuthorizationCredentials=Depends(security)):
#     token=credentials.credentials
#     if token in blacklisted:
#         raise HTTPException(status_code=401,detail='user already blocked')
#     blacklisted.add(token)
#     return {'message':'user logged out successfully'}