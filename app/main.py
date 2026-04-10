from fastapi import FastAPI
from app.database import async_session
import uvicorn


app = FastAPI()

# тестовые эндпоинты

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/user/me")
async def read_user_me():
    return {"user_id": "alisa666"}

@app.get("/user/{user_id}")
async def read_user_me(user_id: int):
    return {"user_id": user_id}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}

# генераторная зависимость 
async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        db.close()

