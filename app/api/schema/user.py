from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: EmailStr = None
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr = None
    password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: str = None


class UserInDBBase(UserBase):
    id: int = None
    is_active: Optional[bool] = True


# Additional properties to return via API
class User(UserInDBBase):
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str