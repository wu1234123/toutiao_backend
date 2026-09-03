from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import alias
from typing import Optional

class UserRequest(BaseModel):
    username:str
    password:str

class UserInfoBase(BaseModel):
    nickname:Optional[str]=Field(None,max_length=50,description="昵称")
    avatar:Optional[str]=Field(None,max_length=255,description="头像URL")
    gender:Optional[str]=Field(None,max_length=10,description="性别")
    bio:Optional[str]=Field(None,max_length=500,description="个人简介")



class UserInfoResponse(BaseModel):
    id:int
    username:str
    bio:Optional[str]=None
    avatar:Optional[str]=None

    model_config=ConfigDict(
        from_attributes=True
    )

class UserAuthResponse(BaseModel):
    token:str
    user_info:UserInfoResponse=Field(...,alias="userInfo")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        by_alias=True
    )


class UserUpdateRequest(BaseModel):
    nickname: str=None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None


class UserChangePasswordRequest(BaseModel):
    old_password: str=Field(...,alias="oldPassword",description="旧密码")
    new_password: str=Field(...,min_length=6,alias="newPassword",description="新密码")
    