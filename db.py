import os
from sqlmodel import SQLModel
from dotenv_vault import load_dotenv
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
load_dotenv()

# DATABASE_URL = "sqlite+aiosqlite:///ResumeBuild.db"
# if not os.environ.get("DATABASE_URL"):
#     os.environ["DATABASE_URL"] = getpass.getpass("Enter API key for OpenAI: ")
#os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("Error: DB URL environment variable not set.")
    raise ValueError("Error: DB URL environment variable not set.")

print(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    async with async_session() as session:
        yield session

