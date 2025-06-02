from celery import Celery
from pydantic_ai import Agent
from dotenv_vault import load_dotenv
from typing import Union
from validation import ResumeData, CompareData
from app_tools import text_extracter
import asyncio
import os
import getpass

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0', result_expires=900)
model_config = {
        "temperature": 0.1,  # Low for structured data
        "top_p": 0.95,       # Balances creativity & focus
        "max_tokens": 1500,  # Sufficient for long resumes
        "frequency_penalty": 0.5,  # Avoids redundant bullet points
        "presence_penalty": 0.5,   # Encourages diverse descriptions
        }


@celery_app.task(name='tasks.struct_agent')
def struct_agent(system_prompt:str,file_path:str):
    agent: Agent[None, Union[ResumeData, str]] = Agent(
    'openai:gpt-4o',
    output_type=Union[ResumeData, str],
    system_prompt=system_prompt,
    model_params=model_config
    )
    raw_resume_text = asyncio.run(text_extracter(file_path))
    result = agent.run_sync(raw_resume_text)
    if isinstance(result.output, ResumeData):
        return result.output.model_dump()  # Use Pydantic's model_dump()
    return result.output


@celery_app.task(name='tasks.compare_agent')
def compare_agent(system_prompt:str,user_info:str):
    agent: Agent[None, Union[CompareData, str]] = Agent(
    'openai:gpt-4o',
    output_type=Union[CompareData, str],
    system_prompt=system_prompt,
    model_params=model_config
    )
    result = agent.run_sync(user_info)
    if isinstance(result.output, CompareData):
        return result.output.model_dump()  # Use Pydantic's model_dump()
    return result.output

@celery_app.task(name='tasks.rebuilt_agent')
def rebuilt_agent(system_prompt:str,user_info:str):
    agent: Agent[None, Union[ResumeData, str]] = Agent(
    'openai:gpt-4o',
    output_type=Union[ResumeData, str],
    system_prompt=system_prompt,
    model_params=model_config
    )
    result = agent.run_sync(user_info)
    if isinstance(result.output, ResumeData):
        return result.output.model_dump()  # Use Pydantic's model_dump()
    return result.output