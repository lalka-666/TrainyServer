from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db, Passenger
from ..schemas import Passenger as Pass
from ..schemas import PassengerResponse

router = APIRouter()

@router.get("/passenger/{user_id}", response_model=PassengerResponse)
async def getPassengers(
        user_id: int,
        db: AsyncSession = Depends(get_db)
):
    result = db.execute(
        select(
            Passenger.passenger_id,
            Passenger.full_name,
            Passenger.document_type,
            Passenger.document_number,
            Passenger.is_default
        ).where(Passenger.user_id == user_id)
    )

    passengers = []
    for row in result.all():
        passengers.append(
            Pass(
                passenger_id=row[0],
                full_name=row[1],
                document_type=row[2],
                document_number=row[3],
                is_default=row[4]
            )
        )
    
    return PassengerResponse(passengers=passengers)