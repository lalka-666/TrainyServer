from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db, Carriage, Seat
from ..schemas import Seat as SeatClass
from ..schemas import SeatResponse

router = APIRouter()

@router.get("/seat", response_model=SeatResponse)
async def seats(
        trip_id: int,
        carriage_number: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Seat.seat_number, Seat.price)
        .join(Carriage, Carriage.carriage_id == Seat.carriage_id)
        .where(Carriage.trip_id == trip_id,
                Carriage.carriage_number == carriage_number,
                Seat.is_available == True)
        .order_by(Seat.seat_number)
    )

    seats = []
    for row in result.all():
        seats.append(
            SeatClass(
                seat_number=row[0],
                price=row[1]
            )
        )

    return SeatResponse(seats=seats)