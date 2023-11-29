from fastapi import FastAPI
from mangum import Mangum
from users import router as user_router
from post import router as post_router
from decouple import config

app = FastAPI()

# Include routes from user.py and post.py using routers
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(post_router, prefix="/posts", tags=["posts"])

SECRET_KEY = config("SECRET_KEY")

# Other routes and application configuration
@app.get("/")
async def about():
    return {"application": "Content-Overflow-API", "version": "0.1"}


handler = Mangum(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
