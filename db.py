import os
from sqlmodel import SQLModel
from dotenv_vault import load_dotenv
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("Error: DB URL environment variable not set.")
    raise ValueError("Error: DB URL environment variable not set.")

print(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, 
                             #echo=True,
                             future=True,
                             # Disable prepared statement caching
                             pool_size=5,
                             max_overflow=5,
                             pool_recycle=1800,
                             pool_pre_ping=True,
                             connect_args={
                                "statement_cache_size": 0,
                                "timeout": 10,
                                "command_timeout": 5
                            })
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    async with async_session() as session:
        yield session

