from celery import Celery
from pydantic_ai import Agent
from dotenv_vault import load_dotenv
from typing import Union
from validation import ResumeData, CompareData
from app_tools import text_extracter
import smtplib
from email.message import EmailMessage
from prompts import otp_format,STRUCT_AGENT_INSTRUCTIONS, COMPARE_AGENT_INSTRUCTIONS
import asyncio
import os
import getpass

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY environment variable not set.")
    raise ValueError("Error: OPENAI_API_KEY environment variable not set.")
celery_app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0', result_expires=900)
#celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0', result_expires=900)

model_config = {
        "temperature": 0.1,  # Low for structured data
        "top_p": 0.95,       # Balances creativity & focus
        "max_tokens": 1500,  # Sufficient for long resumes
        "frequency_penalty": 0.5,  # Avoids redundant bullet points
        "presence_penalty": 0.5,   # Encourages diverse descriptions
        "request_timeout": 30
        }


@celery_app.task(name='tasks.struct_agent',autoretry_for=(Exception,), retry_kwargs={'max_retries': 2}, time_limit=60)
def struct_agent(system_prompt:str,file_path:str):
    agent: Agent[None, Union[ResumeData, str]] = Agent(
    'openai:gpt-4.1',
    output_type=Union[ResumeData, str],
    instructions = STRUCT_AGENT_INSTRUCTIONS,
    system_prompt=system_prompt,
    model_params=model_config
    )
    raw_resume_text = asyncio.run(text_extracter(file_path))
    try:
        result = agent.run_sync(raw_resume_text)
        if isinstance(result.output, ResumeData):
            return result.output.model_dump()  # Use Pydantic's model_dump()
        return result.output
    except Exception as e:
        return {"error": f"LLM failure: {str(e)}"}


@celery_app.task(name='tasks.compare_agent',autoretry_for=(Exception,), retry_kwargs={'max_retries': 2}, time_limit=60)
def compare_agent(system_prompt:str,user_info:str):
    agent: Agent[None, Union[CompareData, str]] = Agent(
    'openai:gpt-4.1-mini',
    output_type=Union[CompareData, str],
    instructions=COMPARE_AGENT_INSTRUCTIONS,
    system_prompt=system_prompt,
    model_params=model_config
    )
    try:
        result = agent.run_sync(user_info)
        if isinstance(result.output, CompareData):
            return result.output.model_dump()  # Use Pydantic's model_dump()
        return result.output
    except Exception as e:
        return {"error": f"LLM failure: {str(e)}"}

@celery_app.task(name='tasks.rebuilt_agent',autoretry_for=(Exception,), retry_kwargs={'max_retries': 2}, time_limit=60)
def rebuilt_agent(system_prompt:str,user_info:str):
    agent: Agent[None, Union[ResumeData, str]] = Agent(
    'openai:gpt-3.5-turbo',
    output_type=Union[ResumeData, str],
    system_prompt=system_prompt,
    model_params=model_config
    )
    try:
        result = agent.run_sync(user_info)
        if isinstance(result.output, ResumeData):
            return result.output.model_dump()  # Use Pydantic's model_dump()
        return result.output
    except Exception as e:
        return {"error": f"LLM failure: {str(e)}"}

@celery_app.task(name='tasks.delete_file')
def delete_file(file_path):
    try:
        os.remove(file_path)
    except Exception as error:
        print(f"error at file delete: {error}")

@celery_app.task(name="task.mail_service",autoretry_for=(Exception,), retry_kwargs={'max_retries': 2})
def mail_service(mailaddress: str,code: int):
    html_content = otp_format(code)
    TO_EMAIL = mailaddress #"puneeth.ku@hashtechinfo.com"  # Replace with your test email (e.g., Gmail)
    FROM_EMAIL = os.getenv("SMTP_USERNAME")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = os.getenv("SMTP_PORT")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    #print(FROM_EMAIL,FROM_EMAIL,SMTP_SERVER,SMTP_PORT,SMTP_PASSWORD)
    if not (SMTP_SERVER and SMTP_PORT and FROM_EMAIL and SMTP_PASSWORD):
        print("❌ Missing SMTP environment config")
        return None
    msg = EmailMessage()
    msg["Subject"] = "🔐 Your OTP Code"
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL
    msg.set_content("This is an HTML email. Please view in HTML-capable client.")  # fallback text
    msg.add_alternative(html_content, subtype='html')
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            #server.set_debuglevel(2)
            server.login(FROM_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"❌ Failed to send email: {e}")