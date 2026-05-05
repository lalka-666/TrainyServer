from fastapi import Depends, APIRouter
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db, Carriage, Seat
from ..schemas import CarrTypeResponse, CarriagesResponse
from ..schemas import Carriage as Carr

router = APIRouter()

@router.get("/carriage/type", response_model=CarrTypeResponse)
async def carriage_types(
    trip_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Carriage.carriage_type)
        .where(Carriage.trip_id == trip_id)
        .distinct()
    )

    carriage_types = result.scalars().all()
    return CarrTypeResponse(carriage_types=carriage_types)


@router.get("/carriage/type/{type}", response_model=CarriagesResponse)
async def carriages(
    type: str,
    trip_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(
            Carriage.carriage_number, 
            Carriage.total_seats,
            func.count(Seat.seat_id).filter(Seat.is_available == True).label("free_seats"))
        .join(Seat, Seat.carriage_id == Carriage.carriage_id)
        .where(Carriage.carriage_type == type, Carriage.trip_id == trip_id)
        .group_by(Carriage.carriage_id)
    )

    carriages = []
    for row in result.all():
        carriages.append(
            Carr(
                carriage_number=row[0],
                number_of_seats=row[1],
                free_seats=row[2]
            )
        )

    return CarriagesResponse(carriages=carriages)