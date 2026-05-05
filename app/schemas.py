from pydantic import BaseModel
from typing import List
from decimal import Decimal


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

class Schedule(BaseModel):
    trip_id: int
    first_station: str
    last_station: str
    departure_time: str
    arrival_time: str
    departure_city: str
    destination_city: str
    destination_time: str


# carriage schemas 
class CarrTypeResponse(BaseModel):
    carriage_types: List[str]

class Carriage(BaseModel):
    carriage_number: int
    number_of_seats: int
    free_seats: int

class CarriagesResponse(BaseModel):
    carriages: List[Carriage]


# seats schemas
class SeatResponse(BaseModel):
    seats: List[Seat]

class Seat(BaseModel):
    seat_number: int
    price: Decimal


# passenger schemas
class Passenger(BaseModel):
    passenger_id: int
    full_name: str
    document_type: str
    document_number: int
    is_default: bool

class PassengerResponse(BaseModel):
    passengers: List[Passenger]