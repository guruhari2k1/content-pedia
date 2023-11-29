from fastapi import Depends, APIRouter, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import get_db
from jwt import encode
from models import User
from entities import UserCreate, UserLogin, VerifyToken
from datetime import datetime, timedelta
import hashlib

# from main import SECRET_KEY
from db import SECRET_KEY


router = APIRouter()
AUTH_METHOD = "AUTH_TOKEN"
SALT = SECRET_KEY
TOKEN_DURATION = 1  # Total duration of a Token in Minutes


@router.post("/token")
async def auth_token(
    form_data: UserLogin,
    db: Session = Depends(get_db),
):
    username = form_data.username
    password = form_data.password

    print("status", await verify_user(username=username, password=password, db=db))

    if await verify_user(username=username, password=password, db=db):
        expiration = timedelta(minutes=TOKEN_DURATION)
        token_creation_time = datetime.utcnow()
        string = f"{username}:{expiration}:{token_creation_time}:{SALT}"
        hashed_token = await tokenize(string=string)
        return {"token": hashed_token, "creation_time": token_creation_time}


async def tokenize(string):
    return hashlib.sha256(string.encode()).hexdigest()


@router.post("/verify")
async def vefiy_token(user: VerifyToken, db: Session = Depends(get_db)):
    if user.username != None:
        db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found !")
    expiration = timedelta(minutes=TOKEN_DURATION)
    if user.creation_time > datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid Creation Time !")
    if expiration + user.creation_time <= datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token Expired or Invalid Token !")
    string = f"{user.username}:{expiration}:{user.creation_time}:{SALT}"
    return user.token == await tokenize(string=string)


async def verify_user(
    username: str = None, password: str = None, email: str = None, db: Session = None
):
    if username != None:
        user = db.query(User).filter(User.username == username).first()
    elif email != None:
        user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found !")
    if not user.check_password(password):
        raise HTTPException(status_code=404, detail="Incorrect Password !")
    else:
        return True


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
        return {
            "token": encode(
                {"username": user.username, "email": user.email},
                SALT,
                algorithm="HS256",
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
