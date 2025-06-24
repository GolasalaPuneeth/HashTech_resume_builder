from fastapi import APIRouter,HTTPException,Depends,status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db import get_session,AsyncSession
from DBModels import User
from sqlmodel import select,update
from validation import UserDetails,ResumeData,EduDetails
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
    result = await get_user_master_data(email, session=session)
    if not result:
        raise HTTPException(status_code=404, detail="Master Data not found")
    try:
        return ResumeData(**json.loads(result))
    except (json.JSONDecodeError, TypeError, Exception) as e:
        raise HTTPException(status_code=500, detail=f"Corrupted resume data in DB. indetail: {e}")


@user_details.put("/Master-data",status_code=status.HTTP_202_ACCEPTED)
async def update_user_master_data(email:str, resume_data:ResumeData, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.exec(select(User).where(User.email == email.lower()))
        user = result.first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.Master_resune_data = json.dumps(resume_data.model_dump())
        await session.commit()
        await session.refresh(user)
        return {"status": True}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Unable to update Data: {str(e)}")
   
@user_details.get("/Master-Edu",status_code=status.HTTP_200_OK,response_model=EduDetails)
async def get_user_Edu(email:str, session: AsyncSession = Depends(get_session)):
    #To use EduDetails(**json.loads(sam))
    try:
        result = await session.exec(select(User).where(User.email == email.lower()))
        edu = result.first()
        if edu is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User not found {e}")
        return EduDetails(**json.loads(edu.Education))
    except Exception as e:
        raise e

@user_details.put("/Master-Edu",status_code=status.HTTP_200_OK)
async def update_user_Edu(email:str,education:EduDetails, session: AsyncSession = Depends(get_session)):
    #To use EduDetails(**json.loads(sam))
    try:
        stmt = (
            update(User)
            .where(User.email == email.lower())
            .values(Education=education.model_dump_json())
            .execution_options(synchronize_session="fetch")  # "fetch", "evaluate", or False
        )
        result = await session.exec(stmt)
        await session.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"Status": "Updated"}
    except Exception as e:
        await session.rollback()        
        raise e