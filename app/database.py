import enum
import datetime
import sqlalchemy.types as _types
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy import Enum as SAEnum
from typing import List
from decimal import Decimal
from sqlalchemy import Numeric

# создание движка
engine = create_async_engine("postgresql+asyncpg://postgres:0000@localhost:5432/trainy_db", echo=True)

# создание фабрики сессий
async_session = async_sessionmaker(engine, expire_on_commit=False)


#################
# МОДЕЛИ ДАННЫХ #
#################

# базовый класс для моделей
class Base(DeclarativeBase):
    pass




# enum для ролей пользователей
class UserRole(enum.Enum):
    ADMIN = "administrator"
    USER = "user_logged"
    
class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] =  mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), name="role_enum", nullable=False)
    phone_number: Mapped[str] = mapped_column(String(17), nullable=False)
    registered_at: Mapped[datetime.datetime] = mapped_column(_types.TIMESTAMP, nullable=False)

    passengers: Mapped[List["Passenger"]] = relationship(back_populates="user")
    orders: Mapped[List["Order"]] = relationship(back_populates="user")





# enum для типов поездов по дистанции
class DistanceType(enum.Enum):
    LONG = "long_distance"
    LOCAL = "local"
    COMMUTER = "commuter"

# enum для типов поездов по скорости
class SpeedType(enum.Enum):
    PASSENGER = "passenger"
    EXPRESS = "express"
    HIGH_SPEED = "high_speed"
    VERY_HIGH_SPEED = "very_high_speed"

class Train(Base):
    __tablename__ = "trains"
    train_id: Mapped[int] = mapped_column(primary_key=True)
    train_number: Mapped[int] = mapped_column(nullable=False)
    train_name: Mapped[str] = mapped_column(nullable=False)
    distance_type: Mapped[DistanceType] = mapped_column(SAEnum(DistanceType), name="dist_t", nullable=False)
    speed_type: Mapped[SpeedType] = mapped_column(SAEnum(SpeedType), name="speed_t", nullable=False)

    trips: Mapped[List["Trip"]] = relationship(back_populates="train")





class CarrType(enum.Enum): 
    SEATED = "seated"
    REVERSED = "reversed"
    GENERAL = "general"
    COMPARTMENT = "compartment"
    LUXURY = "luxury"
    SOFT = "soft"
    INTERNATIONAL_4 = "international4"
    INTERNATIONAL_3 = "international3"

class Carriage(Base):
    __tablename__ = "carriages"
    carriage_id: Mapped[int] = mapped_column(primary_key=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.trip_id"), nullable=False)
    carriage_number: Mapped[int] = mapped_column(nullable=False)
    carriage_type: Mapped[CarrType] = mapped_column(SAEnum(CarrType), name="carr_type", nullable=False)
    total_seats: Mapped[int] = mapped_column(nullable=False)

    trip: Mapped["Trip"] = relationship(back_populates="carriages")
    seats: Mapped[List["Seat"]] = relationship(back_populates="carriage")





class TripStatusType(enum.Enum):
    SCHEDULED = "scheduled"
    BOARDING = "boarding"
    DEPARTED = "departed"
    COMPLETED = "completed"
    DELAYED = "delayed"
    CANCELLED = "cancelled"

class Trip(Base):
    __tablename__ = "trips"
    trip_id: Mapped[int] = mapped_column(primary_key=True)
    train_id: Mapped[int] = mapped_column(ForeignKey("trains.train_id"), nullable=False) 
    status: Mapped[TripStatusType] = mapped_column(SAEnum(TripStatusType), name="tr_st_type", nullable=False)
    base_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    carriages: Mapped[List["Carriage"]] = relationship(back_populates="trip") 
    train: Mapped["Train"] = relationship(back_populates="trips")
    trip_stops: Mapped[List["TripStop"]] = relationship(back_populates="trip")




class Seat(Base):
    __tablename__ = "seats"
    seat_id: Mapped[int] = mapped_column(primary_key=True)
    carriage_id: Mapped[int] = mapped_column(ForeignKey("carriages.carriage_id"), nullable=False)
    seat_number: Mapped[int] = mapped_column(nullable=False)
    is_available: Mapped[bool] = mapped_column(nullable=False, default=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    carriage: Mapped["Carriage"] = relationship(back_populates="seats")
    order: Mapped["Order"] = relationship(back_populates="seat")




class OrderStatusType(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class Order(Base):
    __tablename__ = "orders"
    order_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    passenger_id: Mapped[int] = mapped_column(ForeignKey("passengers.passenger_id"), nullable=False)
    seat_id: Mapped[int] = mapped_column(ForeignKey("seats.seat_id"), nullable=False)
    departure_stop_id: Mapped[int] = mapped_column(ForeignKey("trip_stops.stop_id"), nullable=False)
    arrival_stop_id: Mapped[int] = mapped_column(ForeignKey("trip_stops.stop_id"), nullable=False)
    order_date: Mapped[datetime.datetime] = mapped_column(_types.TIMESTAMP, nullable=False)
    status: Mapped[OrderStatusType] = mapped_column(SAEnum(OrderStatusType), name="order_status", nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    payment: Mapped["Payment"] = relationship(back_populates="order")
    user: Mapped["User"] = relationship(back_populates="orders")
    passenger: Mapped["Passenger"] = relationship(back_populates="order")
    seat: Mapped["Seat"] = relationship(back_populates="order") 
    trip_stops: Mapped[List["TripStop"]] = relationship()

    departure_stop: Mapped["TripStop"] = relationship(
        "TripStop",
        foreign_keys=[departure_stop_id],
        back_populates="departure_orders"
    )

    arrival_stop: Mapped["TripStop"] = relationship(
        "TripStop",
        foreign_keys=[arrival_stop_id],
        back_populates="arrival_orders"
    )





class DocType(enum.Enum):
    PASSPORT = "passport"
    INTERN_PASSPORT = "international_passport"
    BIRTH_CERTIFICATE = "birth_certificate"
    MILITARY_ID = "military_id"
    FOREIGN_CITIZEN_PASSPORT = "foreign_citizen_passport"
    TEMPORARY_IDENTITY_CARD = "temporary_identity_card"

class Passenger(Base):
    __tablename__ = "passengers"
    passenger_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False) 
    full_name: Mapped[str] = mapped_column(nullable=False)
    document_type: Mapped[DocType] = mapped_column(SAEnum(OrderStatusType), name="doc_type", nullable=False)
    document_number: Mapped[str] = mapped_column(nullable=False)
    birthday: Mapped[datetime.date] = mapped_column(_types.DATE, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(17), nullable=False)
    is_default: Mapped[bool] = mapped_column(nullable=False, default=False)

    user: Mapped["User"] = relationship(back_populates="passengers")
    order: Mapped["Order"] = relationship(back_populates="passenger")




class TripStop(Base):
    __tablename__ = "trip_stops"
    stop_id: Mapped[int] = mapped_column(primary_key=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.trip_id"), nullable=False)
    station_id: Mapped[int] = mapped_column(nullable=False)
    arrival_time: Mapped[datetime.datetime] = mapped_column(_types.TIMESTAMP, nullable=False) 
    departure_time: Mapped[datetime.datetime] = mapped_column(_types.TIMESTAMP, nullable=False) 

    trip: Mapped["Trip"] = relationship(back_populates="trip_stops")

    departure_orders: Mapped[List["Order"]] = relationship(
        back_populates="departure_stop",
        foreign_keys=[Order.departure_stop_id]
    )

    arrival_orders: Mapped[List["Order"]] = relationship(
        back_populates="arrival_stop",
        foreign_keys=[Order.arrival_stop_id]
    )







class Station(Base):
    __tablename__ = "stations"
    station_id: Mapped[int] = mapped_column(primary_key=True)
    station_name: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[int] = mapped_column(nullable=False)





class PaymentStatusType(enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"

class Payment(Base):
    __tablename__ = "payments"
    payment_id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    payment_date: Mapped[datetime.datetime] = mapped_column(_types.DATE, nullable=False)
    status: Mapped[PaymentStatusType] = mapped_column(SAEnum(PaymentStatusType), name="pay_status", nullable=False) 
    card_last_digits: Mapped[str] = mapped_column(String(4), nullable=False)

    order: Mapped["Order"] = relationship(back_populates="payment")
