from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from contextlib import asynccontextmanager

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:6543/postgres"

engine = create_async_engine(DATABASE_URL, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@asynccontextmanager
async def get_db():
    session = async_session()
    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()

async def get_db_session():
    async with get_db() as session:
        yield session

app = FastAPI()

@app.get("/")
async def get(db: Session = Depends(get_db_session)):
    result = await db.execute(text("SELECT 1;"))
    return result.scalars().all()
