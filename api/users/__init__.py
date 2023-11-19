from fastapi import APIRouter

router = APIRouter()


@router.get("/all")
async def all_users():
    return {"users":["user1","user2"]}





