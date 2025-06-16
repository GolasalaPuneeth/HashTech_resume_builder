import os
import shutil
import fitz
import docx
import uuid
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from weasyprint import HTML
import redis.asyncio as redis
import random
from typing import Dict, Any

UPLOAD_DIR = "uploads"
PDF_DIR = "generated_pdfs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
#for production use =  redis://redis:6379/0
#redis_client = redis.Redis(host='localhost', port=6379, db=0)
redis_client = redis.Redis(host='redis', port=6379, db=0)


async def generate_six_digit_number():
    return str(random.randint(100000, 999999))

async def save_otp(mail: str, otp: str, ttl: int = 600) -> bool:
    try:
        key = f"otp:{mail}"
        await redis_client.setex(key, ttl, otp)
        return True
    except Exception as e:
        print(f"❌ Failed to save OTP: {e}")
        return False
    
async def verify_otp(mail: str, entered_otp: str) -> bool:
    try:
        key = f"otp:{mail}"
        saved_otp = await redis_client.get(key)
        if not saved_otp:
            return False  # OTP expired or not found
        return saved_otp.decode() == entered_otp
    except Exception as e:
        print(f"❌ OTP verification failed: {e}")
        return False

async def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")
    return text

async def extract_text_from_word(docx_path):
    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"Word document not found: {docx_path}") 
    text = ""
    try:
        doc = docx.Document(docx_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        raise Exception(f"Error extracting text from Word document: {str(e)}")
    return text

async def text_extracter(filePath: str)-> str:
    file_extension = os.path.splitext(filePath)[1].lower()
    if file_extension == ".pdf":
        return await extract_text_from_pdf(filePath)
    elif file_extension in [".docx", ".doc"]:
        return await extract_text_from_word(filePath)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

async def save_file(resume):
    file_extension = os.path.splitext(resume.filename)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    finally:
        # Close the file
        resume.file.close()
        return file_path


# -----------------------------------------------------------------------------------------------------
                                              # ASHMITH #
#------------------------------------------------------------------------------------------------------

async def format_resume_data(data: Dict[str, Any]) -> Dict[str, Any]:
    formatted_data = {}
    
    # Format summary
    if "Professional_Summary" in data:
        formatted_data["summary"] = data["Professional_Summary"]
    
    # Format skills - ensure we're not passing dictionaries with 'items' method
    if "skills" in data:
        formatted_data["skills"] = []
        for skill_category in data["skills"]:
            formatted_skill = {
                "category": skill_category.get("category", ""),
                "skill_items": skill_category.get("items", [])
            }
            formatted_data["skills"].append(formatted_skill)
    
    # Format work experience
    if "work_experiences" in data:
        formatted_data["experience"] = []
        for job in data["work_experiences"]:
            formatted_job = {
                "company": job.get("company", ""),
                "position": job.get("job_title", ""),
                "location": job.get("location", ""),  # Location might not be in the input data
                "description": "\n".join(job.get("description", [])) if isinstance(job.get("description"), list) else job.get("description", "")
            }
            
            # Parse duration into startDate and endDate
            duration = job.get("duration", "")
            if duration and " – " in duration:
                start_date, end_date = duration.split(" – ")
                formatted_job["startDate"] = start_date
                formatted_job["endDate"] = end_date
            else:
                formatted_job["startDate"] = ""
                formatted_job["endDate"] = duration
                
            formatted_data["experience"].append(formatted_job)
    
    # Format projects
    if "projects" in data:
        formatted_data["projects"] = []
        for project in data["projects"]:
            technologies = ", ".join(project.get("technologies", []))
            tech_str = f" ({technologies})" if technologies else ""
            
            formatted_project = {
                "title": project.get("name", "") + tech_str,
                "description": "\n".join(project.get("description", [])) if isinstance(project.get("description"), list) else project.get("description", "")
            }
            formatted_data["projects"].append(formatted_project)
    
    # Add education if present 
    if "education" in data:
        formatted_data["education"] = data["education"]
    else:
        formatted_data["education"] = []
    
    # Add certifications if present
    if "certifications" in data:
        formatted_data["certifications"] = data["certifications"]
    
    # # Add key achievements if present (not in the sample data)
    # if "key_achievements" in data:
    #     formatted_data["keyAchievements"] = data["key_achievements"]
    
    return formatted_data

async def count_value_characters(data):
    total_chars = 0

    if isinstance(data, str):
        total_chars += len(data)
    elif isinstance(data, list):
        for item in data:
            total_chars += await count_value_characters(item)
    elif isinstance(data, dict):
        for value in data.values():
            total_chars += await count_value_characters(value)

    return total_chars

async def get_page_size(characters):
    if characters >= 5000 and characters <=6000:
        # print("characters >= 5000 and characters <=6000")
        return 380
    elif characters >= 4700 and characters <=5000:
        # print("characters >= 4700 and characters <=5000")
        return 350
    elif characters >= 4500 and characters <=4700:
        # print("characters >= 4500 and characters <=4700")
        return 300
    elif characters >= 4200 and characters <=4500:
        # print("characters >= 4200 and characters <=4500")
        return 280
    elif characters >= 4000 and characters <=4200:
        # print("characters >= 4000 and characters <=4200")
        return 260
    return 250

async def generate_resume_from_json(basic_details, resume_data): 
    templates = Jinja2Templates(directory="templates")
    
    PDF_DIR = "generated_pdfs"
    os.makedirs(PDF_DIR, exist_ok=True)
    
    # Generate a unique filename for the PDF
    filename = f"resume_{uuid.uuid4().hex}.pdf"
    pdf_path = os.path.join(PDF_DIR, filename)
    
    # First, ensure resume_data is a dictionary
    if not isinstance(resume_data, dict):
        raise TypeError("resume_data must be a dictionary")
    
    # Ensure basic_details is a dictionary
    if not isinstance(basic_details, dict):
        raise TypeError("basic_details must be a dictionary")
    
    # Format the data according to our template's expected structure
    formatted_data = await format_resume_data(resume_data)
    
    # Create a complete resume object with basicDetails
    complete_resume = formatted_data
    complete_resume["basicDetails"] = basic_details
    complete_resume["pageSize"] = await get_page_size(await count_value_characters(resume_data))

    
    # Render template with the provided data
    html_content = templates.get_template("resume/resume_dynamic.html").render(
        resume=complete_resume
    )
    #resume.basicDetails.name
    try:  
        # Save the HTML content to a temporary file
        temp_html_path = os.path.join(PDF_DIR, f"temp_{uuid.uuid4().hex}.html")
        with open(temp_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"Temporary HTML file created at {temp_html_path}")

        HTML(filename=temp_html_path).write_pdf(
            pdf_path,
        )
        #print(pdf_path)
        #delete_file.apply_async((filepath,), countdown=50)

        # Verify PDF was created and has content
        # if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        #     print(f"PDF generated successfully at {pdf_path}")
        # else:
        #     print(f"PDF generation failed or created empty file at {pdf_path}")
        #     return None
            
        # Clean up the temporary HTML file
        try:
            os.remove(temp_html_path)
            #print(f"Temporary HTML file removed: {temp_html_path}")
        except Exception as e:
            print(f"Warning: Could not remove temporary HTML file: {str(e)}")
            
        # Return the PDF filename and path
        return {
            "download_url": [f"/resume/download/{filename}",pdf_path]
        }
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return None