from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .endpoints import auth, schedule, carriages

app = FastAPI()
app.include_router(auth.router)
app.include_router(schedule.router)
app.include_router(carriages.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           
    allow_credentials=True,
    allow_methods=["*"],           
    allow_headers=["*"],
)