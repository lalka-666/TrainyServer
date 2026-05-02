from fastapi import Depends, APIRouter
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db, Carriage
from ..schemas import CarrTypeResponse

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