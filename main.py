from fastapi import FastAPI,UploadFile,File,HTTPException,status,Body,Depends,Request
from fastapi.responses import JSONResponse, FileResponse,StreamingResponse
from typing import Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from validation import TaskID,ResumeData,JobDescWithID,ResumeAndCurrentTaskID,CompareData,FinalBuilder
from celery.result import AsyncResult
from app_tools import save_file,generate_resume_from_json,PDF_DIR
from AI_agent import struct_agent,celery_app,compare_agent,rebuilt_agent,delete_file
from prompts import convert_struct_prompt,compare_struct_prompt,resume_rebuilt_prompt
from getlogin import auth_router
from user_profile import user_details
from test_func import generate_pdf_bytes_chunked
from db_tools import get_user_master_data
from db import get_session,AsyncSession
import time
import json
import uvicorn
import os

EXPIRE_TIME: int = 300
FILE_EXPIRE: int = 150

app = FastAPI(root_path="/resumeBuilder-Dev",title="Tap My Talent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000
    response.headers["X-Response-Time"] = f"{execution_time:.2f} ms"
    return response

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
async def job_desc(job_desc_with_id: JobDescWithID,session:AsyncSession = Depends(get_session)):
    if job_desc_with_id.task_id:
        struct_data = AsyncResult(job_desc_with_id.task_id,app=celery_app)
        if struct_data.result == None:
            raise HTTPException(status_code=status.HTTP_301_MOVED_PERMANENTLY,detail="Session Expired")
        user_info =f"""Candidate Profile : {struct_data.result} \n Job Description : {job_desc_with_id.job_description}"""
        current_task_id = compare_agent.delay(compare_struct_prompt,user_info)
        return ResumeAndCurrentTaskID(task_id=job_desc_with_id.task_id,match_score_task_id=str(current_task_id))
    struct_data = await get_user_master_data(job_desc_with_id.email,session=session)
    user_info =f"""Candidate Profile : {struct_data} \n Job Description : {job_desc_with_id.job_description}"""
    current_task_id = compare_agent.delay(compare_struct_prompt,user_info)
    return ResumeAndCurrentTaskID(email=job_desc_with_id.email,match_score_task_id=str(current_task_id))

@app.post("/final_builder",response_model = TaskID,status_code=status.HTTP_202_ACCEPTED)
async def final_build(final_data: FinalBuilder,session:AsyncSession = Depends(get_session)):
    if final_data.task_id:
        struct_data = AsyncResult(final_data.task_id,app=celery_app)
        if struct_data.result == None:
            raise HTTPException(status_code=status.HTTP_301_MOVED_PERMANENTLY,detail="Session Expired")    
        user_info =f"""Candidate Profile : {struct_data.result} \n Missing Keywords : {final_data.missing_keywords}"""
        final_taskid = rebuilt_agent.delay(resume_rebuilt_prompt,user_info)
        return TaskID(task_id=str(final_taskid))
    struct_data = await get_user_master_data(final_data.email,session=session)
    user_info =f"""Candidate Profile : {struct_data} \n Missing Keywords : {final_data.missing_keywords}"""
    final_taskid = rebuilt_agent.delay(resume_rebuilt_prompt,user_info)
    return TaskID(task_id=str(final_taskid))

@app.get("/mytest/")
async def ccheck_task():
    # Simulate fetching task logic
    html_content_for_pdf = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chunked Stream PDF</title>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Inter', sans-serif; margin: 40px; background-color: #f0f4f8; color: #2c3e50; }
            .container { max-width: 700px; margin: 0 auto; padding: 25px; background-color: #ffffff; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.15); }
            h1 { color: #1abc9c; border-bottom: 2px solid #1abc9c; padding-bottom: 10px; text-align: center; font-size: 2.2em; margin-bottom: 25px;}
            p { line-height: 1.7; margin-bottom: 12px; font-size: 1.05em; }
            .info-box { background-color: #e8f8f5; border-left: 5px solid #16a085; padding: 15px; border-radius: 8px; margin-top: 20px; font-style: italic; color: #16a085;}
            .footer { margin-top: 40px; text-align: center; font-size: 0.85em; color: #7f8c8d; padding-top: 15px; border-top: 1px dashed #ecf0f1; }
            .highlight-date { font-weight: bold; color: #e74c3c; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Dynamic Report - Chunked Stream</h1>
            <p>This document showcases a PDF being generated by <strong>FastAPI</strong> 
               and <strong>WeasyPrint</strong>, then streamed to your browser in small chunks.</p>
            
            <p class="info-box">
                Generated dynamically on <span class="highlight-date">June 20, 2025</span> 
                at <span class="highlight-date">Hyderabad, Telangana, India</span>.
                The file is sent in <span class="highlight-date">1024-byte chunks</span> for efficient transfer.
            </p>

            <p>This method is ideal for reducing memory footprint on the server during the transfer phase, 
               especially for very large files, and allows the client to start processing data sooner.</p>

            <div class="footer">
                Built for efficiency by Gemini.
            </div>
        </div>
    </body>
    </html>
    """
    pdf_stream_generator = generate_pdf_bytes_chunked(html_content_for_pdf)

    # Return a StreamingResponse.
    # FastAPI will iterate over the generator and send each yielded chunk to the client.
    return StreamingResponse(
        content=pdf_stream_generator,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=chunked_stream_document.pdf"}
    )
    
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
app.include_router(user_details)

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0", port=8000, log_level="info", timeout_keep_alive=600)