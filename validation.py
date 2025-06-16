from pydantic import BaseModel, Field
from typing import List

class TaskID(BaseModel):
    task_id : str

class JobDescWithID(TaskID):
    job_description:str 

class ResumeAndCurrentTaskID(TaskID):
    match_score_task_id: str

class FinalBuilder(TaskID):
    missing_keywords: List[str]

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

class CompareData(BaseModel):
    match_rate: int
    missing_keywords: List[str]
    expected_rate: int

class UserLogin(BaseModel):
    email: str
    password: str