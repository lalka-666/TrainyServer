from fastapi import Depends, APIRouter
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from ..schemas import ScheduleResponse, ScheduleSearch, Schedule
from ..database import get_db, TripStop, Station, Trip

router = APIRouter()

@router.get("/search/schedule", response_model=ScheduleResponse)
async def searchSchedule(
    search_data: ScheduleSearch = Depends(),
    db: AsyncSession = Depends(get_db)
):
    TripStopArr = aliased(TripStop)
    StationArr = aliased(Station)

    result = await db.execute(  
        select(
            TripStop.trip_id,
            Station.city.label("departure_city"),
            StationArr.city.label("destination_city"),
            func.right(TripStop.departure_time, 5).label("departure_time"),
            func.right(TripStop.arrival_time, 5).label("arrival_time"),
            TripStopArr.arrival_time.label("arrival_time")
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
        departure_city = row[1]
        destination_city = row[2]
        departure_time = row[3]
        arrival_time = row[4]
        destination_time = row[5]

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
            arrival_time=arrival_time,
            departure_city=departure_city,
            destination_city=destination_city,
            destination_time=destination_time
        ))

    print(schedules)

    return ScheduleResponse(schedules=schedules)