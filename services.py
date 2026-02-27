from database import collection,database
from schemas import User_details,Get_user
from fastapi import APIRouter, HTTPException,Depends
import bcrypt
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from datetime import datetime,timedelta
from jose import jwt,JWTError
import os
from dotenv import load_dotenv


load_dotenv()


router =APIRouter()

ALGORITHM=os.getenv('ALGORITHM')
SECRET_KEY=os.getenv('SECRET_KEY')
security=HTTPBearer()


@router.post('/register')
async def user_registration(user:User_details):
    if await collection.find_one({'username':user.username}):
        raise HTTPException(status_code=400,detail='user alreaady exist')
    hashed_password=bcrypt.hashpw(user.password.encode(),bcrypt.gensalt())
    print(hashed_password)
    data={"username":user.username,"email":user.email,"password":hashed_password}
    print(data)
    result=await collection.insert_one(data)
    print(result)
    return {'user':'successfully registered'}

@router.post('/login')
async def login(user:User_details):
    existing_user_data=await collection.find_one({'username':user.username})
    if not existing_user_data:
        raise HTTPException(status_code=404,detail='username not found' )
    stored_password = existing_user_data["password"]
    if not bcrypt.checkpw(user.password.encode(),stored_password):
        raise HTTPException(status_code=401,detail='invalid password')
    payload={'user':user.username,
             'email':user.email,
             'exp':datetime.utcnow()+timedelta(minutes=30)}
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    await collection.update_one({'username':user.username},{'$set':{'token':token}})
    return{'access token':token}

@router.get('/verify_token')
async def verify_token(credentials:HTTPAuthorizationCredentials=Depends(security)):
    token=credentials.credentials
    blocked_token= await collection.find_one({'token':token})
    if not blocked_token:
        raise HTTPException(status_code=401,detail='token logged out')
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=403,detail='invalid or expired token')
    
@router.post('/logout')
async def logout(credentials:HTTPAuthorizationCredentials=Depends(security)): 
    token=credentials.credentials
    if not await collection.find_one({'token':token}):
        raise HTTPException(status_code=401,detail='user already logged out')
    await collection.delete_one({'token':token})
    return {'message':'user logged out successfully'}
