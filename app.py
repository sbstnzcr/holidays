import os
from datetime import date, datetime

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Date, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

app = FastAPI()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def get_session():
    async with SessionLocal() as session:
        yield session


Base = declarative_base()


class Feriado(Base):
    __tablename__ = "feriados"

    id = Column(Integer, primary_key=True)
    nombre_feriado = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)
    tipo = Column(String, nullable=False)
    descripción = Column(String, nullable=False)
    dia_semana = Column(String, nullable=False)


class HolidayResponse(BaseModel):
    id: int
    nombre_feriado: str
    fecha: date
    tipo: str
    descripción: str
    dia_semana: str

    class Config:
        from_attributes = True


@app.get("/", response_model=list[HolidayResponse])
async def get_all(session: AsyncSession = Depends(get_session)):
    query = select(Feriado)
    result = await session.execute(query)
    holidays = result.scalars().all()

    return [HolidayResponse.model_validate(holiday) for holiday in holidays]


@app.get("/holiday/{date}", response_model=HolidayResponse)
async def get_holiday(date: str, session: AsyncSession = Depends(get_session)):
    try:
        holiday_date = datetime.strptime(date, "%Y-%m-%d").date()

        query = select(Feriado).where(Feriado.fecha == holiday_date)
        result = await session.execute(query)
        holiday = result.scalar_one_or_none()

        if holiday is None:
            raise HTTPException(status_code=404, detail="Holiday not found")

        return HolidayResponse.model_validate(holiday)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use yyyy-mm-dd.")
