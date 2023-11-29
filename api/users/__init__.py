from fastapi import APIRouter
from .profile import router as profile_router


router = APIRouter()

router.include_router(profile_router, prefix="/profile", tags=["profile"])

@router.get("/all")
async def all_users():
    return {"users":["user1","user2"]}





