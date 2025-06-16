import asyncio
from db import engine
from DBModels import SQLModel  # or import your models directly

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# if __name__ == "__main__":
#     asyncio.run(init_db())
# To migrate to another Database run above code 