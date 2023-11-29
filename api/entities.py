from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class BaseUser(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None


class UserCreate(BaseUser):
    password: str


class UserLogin(BaseUser):
    password: str
    scope: Optional[list] = None


class VerifyToken(BaseUser):
    token:str
    creation_time:datetime

