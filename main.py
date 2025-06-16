from fastapi import FastAPI,UploadFile,File,HTTPException,status,Body
from fastapi.responses import JSONResponse, FileResponse
from typing import Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from validation import TaskID,ResumeData,JobDescWithID,ResumeAndCurrentTaskID,CompareData,FinalBuilder
from celery.result import AsyncResult
from app_tools import save_file,generate_resume_from_json,PDF_DIR
from AI_agent import struct_agent,celery_app,compare_agent,rebuilt_agent,delete_file
from prompts import convert_struct_prompt,compare_struct_prompt,resume_rebuilt_prompt
from getlogin import auth_router
import uvicorn
import os

EXPIRE_TIME: int = 300
FILE_EXPIRE: int = 150

app = FastAPI(root_path="/resumeBuilder-Dev")

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
    delete_file.apply_async((filepath,), countdown=EXPIRE_TIME)
    task = struct_agent.delay(convert_struct_prompt,filepath)
    return TaskID(task_id=task.id)

@app.get("/check-status",response_model=Union[None|str])
def check_task_status(task_id: str  ):
    task_result = AsyncResult(task_id,app=celery_app)
    return task_result.status

@app.get("/get_result",response_model=Union[ResumeData,CompareData])
async def get_task_result(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state != "SUCCESS":
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": task_result.state, "message": str(task_result.result)}
        )
    if isinstance(task_result.result, str):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=task_result.result)
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

# -----------------------------------------------------------------------------------------------------
                                              # ASHMITH #
#------------------------------------------------------------------------------------------------------

@app.post("/generate-resume")
async def generate_resume(
    basic_details: Dict[str, Any] = Body(..., embed=True),
    resume_data: Dict[str, Any] = Body(..., embed=True)
    ):
    try:
        pdf_result = await generate_resume_from_json(basic_details, resume_data)
        print(pdf_result["download_url"][1])
        delete_file.apply_async((pdf_result["download_url"][1],), countdown=FILE_EXPIRE)
        if pdf_result:
            return {
                "pdf": {
                    "download_url": pdf_result["download_url"][0]
                }
            }
    except Exception as error:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(error)
        )
    
@app.get("/resume/download/{filename}")
async def download_pdf(filename: str) -> FileResponse :
    file_path = os.path.join(PDF_DIR, filename)
    if os.path.exists(file_path):
        # Check if file is not empty
        if os.path.getsize(file_path) > 0:
            return FileResponse(
                path=file_path,
                filename=f"{filename}.pdf", 
                media_type="application/pdf",
                headers={
                    "Content-Disposition": "attachment; filename=resume.pdf",
                    "Content-Type": "application/pdf"
                }
            )
        else:
            return JSONResponse(content={"error": "PDF file is empty"}, status_code=500)
    else:
        print(f"PDF file not found: {file_path}")
        return JSONResponse(content={"error": "File not found"}, status_code=404)
    

app.include_router(auth_router)
if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0", port=8000, log_level="info", timeout_keep_alive=600, workers=2)