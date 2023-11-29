from pydantic import BaseModel
from typing import Optional, List



class BaseUser(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None


class UserCreate(BaseUser):
    password: str


class UserLogin(BaseUser):
    password: str
    scope: Optional[list] = None




