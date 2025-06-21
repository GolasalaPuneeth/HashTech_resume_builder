from fastapi import APIRouter,HTTPException,Depends,status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db import get_session,AsyncSession
from DBModels import User
from sqlmodel import select
from validation import UserDetails,ResumeData
import json
from db_tools import get_user_master_data

user_details = APIRouter(prefix="/userDetails", tags=["USER PROFILE DETAILS"])

@user_details.get("/details",status_code=status.HTTP_200_OK,response_model=UserDetails)
async def get_user_details(email:str,session: AsyncSession = Depends(get_session)):
    try:
        result = await session.exec(select(User).where(User.email == email.lower()))
        user = result.first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return(UserDetails(**user.model_dump()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to fetch Data: {e}")
    

@user_details.get("/Master-data",status_code=status.HTTP_200_OK,response_model=ResumeData)
async def get_user_master_data_endpoint(email:str, session: AsyncSession = Depends(get_session)):
    try:
        result = await get_user_master_data(email,session=session)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return ResumeData(**json.loads(result))
    except Exception as e:
        raise e

@user_details.put("/Master-data",status_code=status.HTTP_202_ACCEPTED)
async def update_user_master_data(email:str,resume_data:ResumeData, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.exec(select(User).where(User.email == email.lower()))
        user = result.first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User not found {e}")
        user.Master_resune_data = json.dumps(resume_data)
        await session.commit()
        await session.refresh(user)
        return True
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Unable to update Data: {e}")

