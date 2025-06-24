from db import AsyncSession
from DBModels import User
from sqlmodel import select
from fastapi import HTTPException,status

async def get_user_master_data(email:str, session: AsyncSession):
        result = await session.exec(select(User).where(User.email == email.lower()))
        user = result.first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found: ")
        return user.Master_resune_data