from fastapi import FastAPI,UploadFile,File,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from validation import TaskID,ResumeData,JobDescWithID,ResumeAndCurrentTaskID,CompareData,FinalBuilder
from celery.result import AsyncResult
from app_tools import save_file
from AI_agent import struct_agent,celery_app,compare_agent,rebuilt_agent
from prompts import convert_struct_prompt,compare_struct_prompt,resume_rebuilt_prompt
import uvicorn


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload_file/",response_model=TaskID,status_code=status.HTTP_201_CREATED)
async def get_file(resume: UploadFile = File(...)):
    filepath = await save_file(resume)
    task = struct_agent.delay(convert_struct_prompt,filepath)
    return TaskID(task_id=task.id)

@app.get("/check-status",response_model=Union[None|str])
def check_task_status(task_id: str  ):
    task_result = AsyncResult(task_id,app=celery_app)
    print(type(task_result.status))
    return task_result.status

@app.get("/get_result",response_model=Union[ResumeData,CompareData])
async def get_task_result(task_id:str):
    task_result = AsyncResult(task_id,app=celery_app)
    if task_result.result == None:
        raise HTTPException(status_code=status.HTTP_301_MOVED_PERMANENTLY,detail="Session Expired")
    if isinstance(task_result.result,str):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=task_result.result)
    return task_result.result

@app.post("/job_desc",response_model=ResumeAndCurrentTaskID,status_code=status.HTTP_202_ACCEPTED)
async def job_desc(job_desc_with_id: JobDescWithID):
    struct_data = AsyncResult(job_desc_with_id.task_id,app=celery_app)
    if struct_data.result == None:
        raise HTTPException(status_code=status.HTTP_301_MOVED_PERMANENTLY,detail="Session Expired")
    user_info =f"""Candidate Profile : {struct_data.result} \n Job Description : {job_desc_with_id.job_description}"""
    current_task_id = compare_agent.delay(compare_struct_prompt,user_info)
    return ResumeAndCurrentTaskID(task_id=job_desc_with_id.task_id,match_score_task_id=str(current_task_id))

@app.post("/final_builder",response_model = TaskID,status_code=status.HTTP_202_ACCEPTED)
async def final_build(final_data: FinalBuilder):
    struct_data = AsyncResult(final_data.task_id,app=celery_app)
    if struct_data.result == None:
        raise HTTPException(status_code=status.HTTP_301_MOVED_PERMANENTLY,detail="Session Expired")    
    user_info =f"""Candidate Profile : {struct_data.result} \n Missing Keywords : {final_data.missing_keywords}"""
    final_taskid = rebuilt_agent.delay(resume_rebuilt_prompt,user_info)
    return TaskID(task_id=str(final_taskid))

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")