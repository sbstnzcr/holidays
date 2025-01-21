import asyncio
import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from sqlalchemy import Column, Date, Integer, MetaData, String, Table
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

metadata = MetaData()

feriados = Table(
    "feriados",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre_feriado", String, nullable=False),
    Column("fecha", Date, nullable=False),
    Column("tipo", String, nullable=False),
    Column("descripción", String, nullable=False),
    Column("dia_semana", String, nullable=False),
)


async def create_database_and_tables():
    engine = create_async_engine(DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(metadata.create_all)
        print("Tables created successfully!")

    await engine.dispose()

weekdays = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo",
}

async def insert_data():
    engine = create_async_engine(DATABASE_URL, echo=True)

    url = "https://apis.digital.gob.cl/fl/feriados/2024"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "es-CL,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    async with engine.begin() as conn:
        for holiday in data:
            date = datetime.strptime(holiday["fecha"], "%Y-%m-%d").date()
            day = date.strftime("%A")
            query = feriados.insert().values(
                nombre_feriado=holiday["nombre"],
                fecha=date,
                tipo=holiday["tipo"],
                descripción=holiday["nombre"],
                dia_semana=weekdays[day],
            )
            await conn.execute(query)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_database_and_tables())
    asyncio.run(insert_data())
