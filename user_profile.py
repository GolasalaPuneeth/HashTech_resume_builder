from fastapi import APIRouter,HTTPException,Depends,status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db import get_session,AsyncSession
from DBModels import User
from sqlmodel import select
from validation import UserDetails

user_details = APIRouter(prefix="/userDetails", tags=["USER PROFILE DETAILS"])

@user_details.get("/user",status_code=status.HTTP_200_OK)
async def get_user_details(email:str, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.exec(select(User).where(User.email == email.lower()))
        user = result.first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        # user_details:UserDetails = UserDetails(**user.model_dump())
        return {"message": user}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Unable to fetch Data: {e}")