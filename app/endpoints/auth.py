from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy import select
from ..schemas import ScheduleResponse, ScheduleSearch, Schedule, UserCreate, UserResponse, UserLogin
from ..database import get_db, User, TripStop, Station, Trip
from datetime import datetime
from fastapi import APIRouter

router = APIRouter()


@router.post("/auth/register", response_model=UserResponse)
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


@router.post("/auth/login", response_model=UserResponse)
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


