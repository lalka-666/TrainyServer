from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy import func
from sqlalchemy import select
from .schemas import ScheduleResponse, ScheduleSearch, Schedule, UserCreate, UserResponse, UserLogin
from .database import get_db, User, TripStop, Station, Trip
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           
    allow_credentials=True,
    allow_methods=["*"],           
    allow_headers=["*"],           
)

@app.post("/auth/register", response_model=UserResponse)
async def userRegister(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(400, "User already exist")
    
    new_user = User(
        email=user.email,
        full_name=user.full_name,
        password=user.password,
        role="user_logged",
        phone_number="",
        registered_at=datetime.now()
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@app.post("/auth/login", response_model=UserResponse)
async def userLogin(user: UserLogin, db: AsyncSession = Depends(get_db)):
    select_user = await db.execute(select(User).where(User.email == user.email))
    existing_user = select_user.scalar_one_or_none()

    if existing_user is None or existing_user.password != user.password:
        raise HTTPException(400, "Invalid email or password")
    
    return UserResponse(
        id=existing_user.user_id,
        email=existing_user.email,
        full_name=existing_user.full_name
    )


@app.get("/search/schedule", response_model=ScheduleResponse)
async def searchSchedule(
    search_data: ScheduleSearch = Depends(),
    db: AsyncSession = Depends(get_db)
):
    TripStopArr = aliased(TripStop)
    StationArr = aliased(Station)

    result = await db.execute(  
        select(
            TripStop.trip_id,
            func.right(TripStop.departure_time, 5).label("departure_time"),
            func.right(TripStop.arrival_time, 5).label("arrival_time")
        )
        .join(Station, TripStop.station_id == Station.station_id)
        .join(Trip, TripStop.trip_id == Trip.trip_id)
        .where(
            Station.station_name == search_data.departure_station,
            TripStop.departure_time.like(f"{search_data.departure_date}%")
        )
        .join(TripStopArr, TripStop.trip_id == TripStopArr.trip_id)
        .join(StationArr, TripStopArr.station_id == StationArr.station_id)
        .where(
            StationArr.station_name == search_data.arrival_station,
            TripStop.stop_order < TripStopArr.stop_order
        )
    )
    
    schedules = []
    rows = result.all()

    for row in rows:
        trip_id = row[0]
        departure_time = row[1]
        arrival_time = row[2]

        first = await db.execute(
            select(Station.station_name)
            .join(TripStop, TripStop.station_id == Station.station_id)
            .where(TripStop.trip_id == trip_id)
            .order_by(TripStop.stop_order.asc())
            .limit(1)
        )
        first_station = first.scalar()

        last = await db.execute(
            select(Station.station_name)
            .join(TripStop, TripStop.station_id == Station.station_id)
            .where(TripStop.trip_id == trip_id)
            .order_by(TripStop.stop_order.desc())
            .limit(1)
        )
        last_station = last.scalar()

        schedules.append(Schedule(
            trip_id=trip_id,
            first_station=first_station,
            last_station=last_station,
            departure_time=departure_time,
            arrival_time=arrival_time
        ))

    print(schedules)

    return ScheduleResponse(schedules=schedules)