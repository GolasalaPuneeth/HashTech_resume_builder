# Use the official Python 3.12 image
FROM python:3.12-slim
WORKDIR /HashTech_resume_builder
COPY . .
RUN pip install -r reqriments.txt
RUN apt-get update && apt-get install -y libglib2.0-dev && apt-get install -y libpango1.0-dev
CMD ["python", "main.py"]
