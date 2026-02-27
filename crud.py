from  fastapi import APIRouter, FastAPI,APIRouter,HTTPException,Depends
import bcrypt
from schemas import User_details,Get_user,add_user,updating_user
from database import collection
from datetime import datetime,timedelta
from jose import jwt,JWTError
import os
from dotenv import load_dotenv
from services import verify_token
load_dotenv()


crud=APIRouter()

@crud.get('/user-details',response_model=Get_user)
async def get_user(username:str):
    existing_user_data= await collection.find_one({'username':username})
    if not existing_user_data:
        raise HTTPException(status_code=404,detail='User not found')
    existing_user_data.pop('_id',None)
    return Get_user(**existing_user_data)   


@crud.get('/list')
async def list_user(current_user=Depends(verify_token)):
    all_users=await collection.find({},{'_id':0,'password':0,'token':0}).to_list(length=None)
    return {'logged user':current_user['user'],'all_users':all_users}

@crud.delete('/delete')
async def delete_user(current_user:dict=Depends(verify_token)):
    username=current_user['user']
    if not await collection.find_one({'username':username}):
        raise HTTPException(status_code=404,detail='user not found')
    await collection.delete_one({'username':username})
    return {'status':'success','deleted_user':username}

@crud.post('/add_user')
async def add_user(new_user:add_user,user:dict=Depends(verify_token)):
    if await collection.find_one({'username':new_user.username}):
        raise HTTPException(status_code=400,detail='user already exists')
    hashed_password=bcrypt.hashpw(new_user.password.encode(),bcrypt.gensalt()).decode()
    data={"username":new_user.username,"email":new_user.email,"password":hashed_password}
    result=await collection.insert_one(data)
    return {'message':f'user {new_user.username} added successfully'}

@crud.put('/update_user')
async def update_user(update_user:updating_user,user:dict=Depends(verify_token)):
    existing_user=await collection.find_one({'username':user['user']})
    if not existing_user:
        raise HTTPException(status_code=404,detail='user not found')
    update_data={}
    if update_user.newusername:
        already_user=await collection.find_one({'username':update_user.newusername})
        if already_user:
            raise HTTPException(status_code=400,detail='username already exists')
        update_data['username']=update_user.newusername
    if update_user.newpassword:
            hashed_password=bcrypt.hashpw(update_user.newpassword.encode(),bcrypt.gensalt()).decode()
            update_data['password']=hashed_password
    if not update_data:
        raise HTTPException(status_code=400,detail='no data provided for update')
    try:
        result=await collection.update_one({'username':user['user']},{'$set':update_data})
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    if result.matched_count==0:
        raise HTTPException(status_code=404,detail='user not found')
    return {'message':'user updated successfully'}