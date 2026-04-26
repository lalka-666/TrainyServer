from fastapi import FastAPI

app = FastAPI()

# тестовые эндпоинты

# @app.get("/")
# async def root(db: Session = Depends(get_db)):
#     try:
#         result = db.execute(text("SELECT 1"))
#         return {"status": "ok"}
#     except Exception as e:
#         return {"status": "ok", "message": "db connected!"}


# @app.get("/user/me")
# async def read_user_me():
#     return {"user_id": "alisa666"}

# @app.get("/user/{user_id}")
# async def read_user_me(user_id: int):
#     return {"user_id": user_id}

# @app.get("/items/{item_id}")
# async def get_item(item_id: int):
#     return {"item_id": item_id}





