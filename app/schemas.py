from pydantic import BaseModel
from typing import List


# authorisation schemas
class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    email: str
    full_name: str

class UserLogin(BaseModel):
    email: str
    password: str



# search schemas
class ScheduleSearch(BaseModel):
    departure_station: str
    arrival_station: str
    departure_date: str

class ScheduleResponse(BaseModel):
    schedules: List[Schedule]

# so far so
class Schedule(BaseModel):
    trip_id: int
    first_station: str
    last_station: str
    departure_time: str
    arrival_time: str

class CarriageTypes(BaseModel):
    id: int
    name: str