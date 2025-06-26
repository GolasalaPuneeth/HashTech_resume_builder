from pydantic import BaseModel, Field, model_validator
from typing import List,Optional

class TaskID(BaseModel):
    task_id : str

class JobDescWithID(BaseModel):
    task_id: Optional[str] = None
    email:Optional[str] = None
    job_description:str 
    @model_validator(mode='after')
    def validate_at_least_one(self):
        if not self.task_id and not self.email:
            raise ValueError("Either 'task_id' or 'email' must be provided")
        return self

class ResumeAndCurrentTaskID(BaseModel):
    match_score_task_id: str
    task_id:Optional[str] = None
    email:Optional[str] = None
    @model_validator(mode='after')
    def validate_at_least_one(self):
        if not self.task_id and not self.email:
            raise ValueError("Either 'task_id' or 'email' must be provided")
        return self

class FinalBuilder(BaseModel):
    missing_keywords: List[str]
    task_id:Optional[str] = None
    email:Optional[str] = None
    @model_validator(mode='after')
    def validate_at_least_one(self):
        if not self.task_id and not self.email:
            raise ValueError("Either 'task_id' or 'email' must be provided")
        return self

class WorkExperience(BaseModel):
    job_title: str
    company: str
    duration: str
    description: List[str]
    
class SkillCategory(BaseModel):
    category: str
    items: List[str]
    
class Project(BaseModel):
    name: str
    technologies: List[str]
    description: List[str]
    
class ResumeData(BaseModel):
    work_experiences: List[WorkExperience]
    skills: List[SkillCategory]
    projects: List[Project]
    Professional_Summary : str
    Year_of_experience: int

class EduInfo(BaseModel):
    institution:Optional[str] = None
    location:Optional[str] = None
    degree:Optional[str] = None
    startDate:Optional[str] = None
    endDate:Optional[str] = None

class CertificateInfo(BaseModel):
    Title:Optional[str] = None
    Desc: Optional[str] = None

class EduDetails(BaseModel):
    Education:List[EduInfo]
    Certifications: List[CertificateInfo]

class CompareData(BaseModel):
    match_rate: int
    missing_keywords: List[str]
    expected_rate: int

class UserLogin(BaseModel):
    email: str
    password: str

class UserDetails(BaseModel):
    name: str
    email: str
    phone_number: str

class LoginResponse(BaseModel):
    status:str
    name:str
    email:str