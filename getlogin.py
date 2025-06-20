from fastapi import APIRouter,HTTPException,Depends,status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app_tools import save_otp,verify_otp,generate_six_digit_number
from AI_agent import mail_service
from db import get_session,AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from validation import UserLogin
from sqlmodel import select
from DBModels import User


auth_router = APIRouter(prefix="/auth", tags=["AUTHENTICATION"])
auth_scheme = HTTPBearer()

async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    VALID_TOKEN = await verify_otp(credentials.credentials,"Active")
    if not VALID_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return credentials.credentials


@auth_router.post("/user/register",status_code=status.HTTP_201_CREATED,dependencies=[Depends(validate_token)])
async def create_user(user: User, session: AsyncSession = Depends(get_session)):
    try:
        user.email = user.email.lower()
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    except Exception as e:
        await session.rollback()
        #print(f"❌ Error creating user: {e}")
        raise HTTPException(status_code=500, detail=f"Error while creating user{e}")

@auth_router.put("/user/forgotpass",status_code=status.HTTP_202_ACCEPTED,dependencies=[Depends(validate_token)])
async def update_password(email:str,new_password:str,session: AsyncSession = Depends(get_session)):
    try:
        result = await session.exec(select(User).where(User.email == email.lower()))
        user = result.first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.password = new_password  # NOTE: hash the password in real applications!
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return {"message": "Password updated successfully"}
    except Exception as e:
        await session.rollback()
        print(f"❌ Error updating password: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update password: {e}")
    
@auth_router.get("/user/Checkmail")#,dependencies=[Depends(validate_token)])
async def check_mail(email:str,session: AsyncSession = Depends(get_session)):
    try:
        result = await session.exec(select(User).where(User.email == email.lower()))
        user = result.first()
        if user:
            raise HTTPException(status_code=status.HTTP_306_RESERVED, detail="User found")
        return {"message": "No User Found"}
    except Exception as e:
        await session.rollback()
        print(f"❌ Error: {e}")
        raise e


@auth_router.post("/user/login")
async def login(login_details: UserLogin, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.exec(select(User).where(User.email == login_details.email.lower()))
        user = result.first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if user.password != login_details.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password"
            )
        return {"login": "SUCCESS", "user_email": user.email}
    except Exception as e:
        await session.rollback()
        raise e

@auth_router.post("/send-otp/")
async def send_otp_api(email: str):
    otp = await generate_six_digit_number()
    success = await save_otp(email.lower(), otp)
    mail_service.apply_async(args=[email, otp])
    return {"status": "ok" if success else "fail"}


@auth_router.post("/verify-otp/")
async def verify_otp_api(email: str, otp: str):
    if await verify_otp(email.lower(), otp):
        await save_otp(email.lower()+otp,"Active")
        return {"valid": True}
    return {"valid": False}

