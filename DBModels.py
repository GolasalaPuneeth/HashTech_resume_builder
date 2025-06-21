from sqlmodel import SQLModel, Field, Column, String
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional

class User(SQLModel, table=True):
    __tablename__="User_MasterData"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(sa_column=Column("email", String, unique=True, nullable=False))
    password: str
    phone_number: str
    Master_resune_data: str
