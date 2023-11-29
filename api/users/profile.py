from fastapi import Depends, APIRouter, HTTPException, Request
from sqlalchemy.orm import Session
# from . import router
from db import get_db
from jwt import encode
from models import User
from entities import UserCreate, UserLogin
# from main import SECRET_KEY
from db import SECRET_KEY



router = APIRouter()
AUTH_METHOD = "AUTH_TOKEN"
token = SECRET_KEY

@router.post("/login")
async def auth_user(
    unauth_user: UserLogin, db: Session = Depends(get_db), request: Request = Request
):
    
    user = db.query(User).filter(User.username == unauth_user.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found !")
    if not user.check_password(unauth_user.password):
        raise HTTPException(status_code=404, detail="Incorrect Password !")
    if AUTH_METHOD == "AUTH_TOKEN":
        print(AUTH_METHOD)

    elif AUTH_METHOD == "JWT":
        return  {
            "token": encode(
                {"username": user.username, "email": user.email}, token, algorithm="HS256"
            )
        }
    else:
        raise HTTPException(status_code=401, detail="no auth method provided")







@router.post("/create")
async def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    ext_user = db.query(User).filter(User.email == new_user.email).first()
    if ext_user:
        raise HTTPException(status_code=404, detail="User alread exists !")
    obj = User(username=new_user.username, email=new_user.email)
    obj.set_password(new_user.password)
    db.add(obj)
    db.commit()
    return {"status": "success", "message": "User Created !"}
