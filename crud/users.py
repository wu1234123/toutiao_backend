
from unittest import result

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import  AsyncSession
from models.users import User, UserToken
from datetime import  datetime
from schemas.users import UserRequest, UserUpdateRequest
from utils import security
import uuid
from sqlalchemy import update

from datetime import timedelta

async def get_user_by_username(db:AsyncSession,username:str):
    query=select(User).where(User.username==username)
    result=await  db.execute(query)
    return result.scalar_one_or_none()


async def create_user(db:AsyncSession,user_data:UserRequest):
    hashed_password=security.get_hash_password(user_data.password)
    user=User(username=user_data.username,password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def create_token(db:AsyncSession,user_id:int):
    token=str(uuid.uuid4())
    expires_at=datetime.now()+timedelta(days=7)
    query=select(UserToken).where(UserToken.user_id==user_id)
    result=await db.execute(query)
    user_token=result.scalar_one_or_none()

    if user_token:
        user_token.token=token
        user_token.expires_at=expires_at
        await db.commit()
    else:
        user_token=UserToken(user_id=user_id,token=token,expires_at=expires_at)
        db.add(user_token)
        await db.commit()

    return token


async def authenticate_user(db:AsyncSession,username:str,password:str):
    user=await get_user_by_username(db,username)
    if not user:
        return None
    if not security.verify_password(password,user.password):
        return None

    return user


async def get_user_by_token(db:AsyncSession,token:str):
    """根据token查询用户，同时验证token是否过期"""
    from sqlalchemy import and_
    query = select(UserToken).where(
        and_(UserToken.token == token, UserToken.expires_at > datetime.now())
    )
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if not user_token:
        return None
    user = await db.get(User, user_token.user_id)
    return user


async def update_user(db:AsyncSession,username:str,user_data:UserUpdateRequest):
    query=update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none=True

    ))
    result=await db.execute(query)
    await db.commit()

    if result.rowcount==0:
        raise HTTPException(status_code=404,detail="用户不存在")

    updated_user=await get_user_by_username(db,username)
    return updated_user

async def change_password(db:AsyncSession,user:User,old_password:str,new_password:str):
    if not security.verify_password(old_password,user.password):
        return False
    hashed_new_pwd=security.get_hash_password(new_password)
    user.password=hashed_new_pwd
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True
        