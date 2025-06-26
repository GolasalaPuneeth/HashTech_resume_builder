convert_struct_prompt = """
You are an expert at extracting structured information from resumes. Extract the following data:

1. Work Experiences:
   - For each position: job title, company, duration (employment period)
   - Include all bullet points under each position as description items

2. Skills:
   - Group skills by their categories (Programming Languages, Web Frameworks, etc.)
   - For each category, list all individual skills

3. Projects:
   - For each project: project name, list of technologies used
   - Include all description bullet points

4. Professional_Summary:
    - Get 'Professional Summary' 

5. Years_of_experience:
    - Extract years of experience if available or extract based on work experiences  


"Extract me the requriments of a ResumeData,"
"if you can't extract all data, ask the user to try again."

"""

compare_struct_prompt = """

You are an expert in Human Resources and Applicant Tracking Systems (ATS). You will be provided with two inputs:

   1. A Job Description (JD)

   2. A Candidate Profile, including Work Experience, Skills, Projects, Professional Summary, and Total Years of Experience.

Your task is to analyze and compare the JD and Candidate Profile to extract the following insights:

   1. Match Rate (0 - 100 scale):
      - Evaluate how well the candidate's profile aligns with the job description. Provide a numerical match score (0 to 100) based on relevance, overlap in skills/tools/technologies, and role fit.
   
   2. Missing Keywords:
      Identify important keywords from the job description that are absent or underrepresented in the candidate's data.
      
      Guidelines for keyword selection:

      - Focus strictly on nouns or noun phrases (e.g., tools, technologies, frameworks, platforms).
      - Avoid or minimize verbs, soft skills, or general terms (e.g., "collaborated", "communication", "team player").
      - The list should only include high-impact technical terms that can significantly improve alignment.

   3. Expected Match Rate (Post-Enhancement):
      - Predict the revised match rate (0-100 scale) if the missing keywords are effectively integrated into the candidate's profile.

Important: Analyze both the Job Description and Candidate Profile thoroughly and return only the structured, concise, and insight-driven output as requested.

"Extract me the requriments of a CompareData,"
"if you can't extract all data, ask the user to try again.

"""

resume_rebuilt_prompt = """

You are an expert in Resume Writing, Applicant Tracking Systems (ATS) optimization, and professional content enhancement. You will be provided with six key inputs:

   1. Work Experiences
      - Includes job title, company, employment period, and bullet-point descriptions for each position.

   2. Skills
      - Categorized skills (e.g., Programming Languages, Web Frameworks) with all relevant tools/technologies listed.

   3. Projects
      - Includes project name, technologies used, and bullet-point descriptions.

   4. Professional Summary
      - A short summary of the candidate’s profile.

   5. Years of Experience
      - Overall years of experience provided or inferred from work history.

   6. Missing Keywords
      - A list of critical tools, platforms, or technologies missing in the current resume.

Your Task:

   Analyze all six inputs and generate an ATS-optimized version of the candidate's profile by:

      - Enhancing the resume content using the provided missing keywords in a natural, relevant, and contextual manner.
      - Maintaining clarity, readability, and professionalism while integrating missing terms.
      - Ensuring consistency and completeness across all sections.
      - Inferring missing details (e.g., years of experience, relevant achievements) based on other available inputs.
      - Leaving the Projects section empty only if no project data is provided.

Final Output Structure:

   Return a clean, structured version of the updated candidate profile with the following format:

      Work Experiences
         For each position:
            - Job Title, Company, Employment Period
            - Bullet-pointed responsibilities/achievements (integrated with relevant missing keywords)

      Skills
         - Organized into categories (e.g., Programming Languages, Databases, Cloud Platforms)
         - Enhanced with applicable missing tools or technologies

      Projects
         If provided:
            - Project Name, Technologies Used
            - Bullet-pointed descriptions showcasing problem-solving, implementation, or outcomes
         If not provided: Leave section empty

      Professional Summary
         - A concise, compelling summary tailored to the role, improved with relevant terminology and focus areas

      Years of Experience
         - Explicitly stated, either from input or inferred from employment history

Important Notes:
   - Focus only on technical tools, technologies, platforms, or frameworks while using missing keywords.
   - Do not add soft skills unless explicitly mentioned.
   - Keep the output concise, structured, and ATS-readable (i.e., no fancy formatting or emojis).
   - Return only the updated candidate profile as per the structure above. 

"Extract me the requriments of a ResumeData,"
"if you can't extract all data, ask the user to try again."

"""

def otp_format(otp:str)->str:
    html_format = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTP Verification - Tap My Talent</title>
    <!--[if mso]>
    <noscript>
        <xml>
            <o:OfficeDocumentSettings>
                <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
        </xml>
    </noscript>
    <![endif]-->
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5; line-height: 1.6;">
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f5f5f5;">
        <tr>
            <td align="center" style="padding: 20px 0;">
                
                <!-- Main Container -->
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #FF9999  0%, #E66868 100%); background-color: #E66868; padding: 30px 20px; text-align: center;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                <tr>
                                    <td style="text-align: center;">
                                        <h1 style="font-size: 28px; font-weight: bold; margin: 0 0 10px 0; letter-spacing: 1px; color: #ffffff;">Tap My Talent</h1>
                                        <p style="font-size: 16px; margin: 0; color: #ffffff; opacity: 0.9;">Verification Code</p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 30px; text-align: center;">
                            
                            <h2 style="font-size: 24px; color: #333; margin: 0 0 20px 0; font-weight: 600;">Verify Your Account</h2>
                            
                            <p style="font-size: 16px; color: #666; margin: 0 0 30px 0; line-height: 1.6;">
                                We've received a request to verify your account. Please use the One-Time Password (OTP) below to complete your verification.
                            </p>
                            
                            <!-- OTP Container -->
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: 30px 0;">
                                <tr>
                                    <td align="center">
                                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="background: linear-gradient(135deg, #FF9999  0%, #E66868 100%); background-color: #E66868; border-radius: 8px; padding: 25px;">
                                            <tr>
                                                <td style="text-align: center;">
                                                    <p style="color: #ffffff; font-size: 14px; font-weight: 600; margin: 0 0 10px 0; text-transform: uppercase; letter-spacing: 1px;">Your OTP Code</p>
                                                    <p style="font-size: 36px; font-weight: bold; color: #ffffff; letter-spacing: 8px; margin: 10px 0; font-family: 'Courier New', monospace;">{otp}</p> <!-- Dynamically Rerplace the OTP Here -->
                                                    <p style="color: #ffffff; font-size: 14px; margin: 15px 0 0 0; opacity: 0.9;">Select and copy the code above</p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Validity Warning -->
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: 25px 0;">
                                <tr>
                                    <td style="background-color: #fff5f5; border: 2px solid #E66868; border-radius: 8px; padding: 15px;">
                                        <p style="margin: 0; color: #b91c1c; font-size: 14px; text-align: center;">
                                            <span style="font-size: 18px; margin-right: 8px;">⏰</span>
                                            <strong>Important:</strong> This OTP is valid for <strong>10 minutes</strong> only. Please complete your verification before it expires.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="font-size: 14px; color: #888; margin: 30px 0 0 0; line-height: 1.5;">
                                If you didn't request this verification code, please ignore this email or contact our support team if you have concerns about your account security.
                            </p>
                            
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 25px 30px; text-align: center; border-top: 1px solid #e9ecef;">
                            <p style="font-size: 12px; color: #6c757d; line-height: 1.5; margin: 0;">
                                This is an automated message from <span style="font-weight: bold; color: #E66868;">Tap My Talent</span>.<br>
                                Please do not reply to this email as this mailbox is not monitored.<br>
                                For support, please contact us through our website or support channels.
                            </p>
                        </td>
                    </tr>
                    
                </table>
                
            </td>
        </tr>
    </table>
</body>
</html>

"""
    return html_format

STRUCT_AGENT_INSTRUCTIONS = """
You are an expert at extracting structured information from resumes.

If the content provided is clearly not a resume (e.g., unrelated text, empty content, or lacks work experience and skills),
**DO NOT attempt to extract anything.**
Instead, clearly respond with the following:
"Uploaded content is not related to a resume. Please upload a valid resume document."

Otherwise, extract:
1. Work Experiences - title, company, duration, descriptions
2. Skills - grouped by category
3. Projects - name, technologies, bullet points
4. Professional Summary
5. Years of Experience - explicitly stated or inferred from timeline
"""

COMPARE_AGENT_INSTRUCTIONS = """
You are an expert in Human Resources and Applicant Tracking Systems (ATS). You will be given two inputs:

1. A Job Description (JD)
2. A Candidate Profile (including Work Experience, Skills, Projects, Professional Summary, and Total Years of Experience)

Your job is to deeply analyze and compare these two inputs and return insights as a structured JSON object with the following fields:

1. match_rate: (int, 0–100 scale)
   - Numerically rate how well the candidate's profile aligns with the JD.
   - Use overlap of skills, technologies, tools, role fit, and keyword presence as criteria.
   - Example: 78

2. missing_keywords: (List of str)
   - List important **nouns or noun phrases** from the JD that are **absent or underrepresented** in the candidate profile.
   - Focus only on technical/role-critical terms like tools, technologies, platforms.
   - Avoid verbs, soft skills, or general terms (e.g., “teamwork”, “collaboration”).

3. expected_match_rate: (int, 0–100 scale)
   - Estimate the new match score **after** the candidate hypothetically incorporates the missing keywords effectively.
   - Example: 85

If either the job description or candidate profile is missing or unrelated, return:
{ "error": "Job Description or Candidate Profile not provided or not relevant. Please check the input." }

Only return the structured result. Do not include any additional text or explanation.
"""
