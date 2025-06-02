from prompts import resume_rebuilt_prompt
from AI_agent import rebuilt_agent


miskey = ['Node.js', 'Go', 'Azure', 'Domain-Driven Design (DDD)']

res_data = {
  "work_experiences": [
    {
      "job_title": "Senior Software Engineer",
      "company": "Federal Soft Systems",
      "duration": "SEP 2021 – OCT 2024",
      "description": [
        "Developed Python-based tools for both Hardware (raspberry pi) and Cloud APIs (Aws)",
        "Development of innovative products while also managing the optimization of existing product workflows",
        "Designed, developed, and maintained RESTful APIs using Python and FastAPI, adhering to best practices for scalable and efficient backend systems.",
        "Built and optimized database interactions using relational (PostgreSQL/MySQL) and NoSQL (MongoDB) databases, implementing robust data models.",
        "Integration of third-party APIs and services, ensuring seamless data exchange and system interoperability.",
        "Troubleshot and debugged production issues, applying performance optimization techniques to enhance API stability and response times."
      ]
    },
    {
      "job_title": "Senior Executive Engineer",
      "company": "Barron TechServ Ltd (OKI Pvt Ltd), Chennai",
      "duration": "FEB 2020 – SEP 2021",
      "description": [
        "I excel in managing comprehensive computer hardware and software troubleshooting processes",
        "I ensure seamless server connectivity via IP networks, efficiently collect EJ files, and implement robust data transmission protocols.",
        "Entrusted with providing exemplary level 1 and 2 support to both clients and team members.",
        "Expertise in configuring routers, switches, and firewalls for secure data flow"
      ]
    },
    {
      "job_title": "Verification officer",
      "company": "Writer information Pvt LTD, Hyderabad",
      "duration": "APR 2019 – JAN 2020",
      "description": [
        "Successfully collaborated with leading clients such as TVS Credit Sathi, Kotak, Bajaj Auto Finance, and Shriram Chits to deliver tailored solutions.",
        "Partnered with industry leaders like TVS Credit Sathi, Kotak, Bajaj Auto Finance, and Shriram Chits to implement customized solutions.",
        "Led a team to drive efficient and productive field operations."
      ]
    }
  ],
  "skills": [
    {
      "category": "Programming Languages",
      "items": [
        "Python 3",
        "JS",
        "C"
      ]
    },
    {
      "category": "Web Frameworks",
      "items": [
        "Django",
        "Flask",
        "FastAPI",
        "Express"
      ]
    },
    {
      "category": "Databases",
      "items": [
        "PostgreSQL",
        "SQL Alchemy",
        "Pymysql",
        "Pymongo",
        "VectorDB",
        "Redis_cache"
      ]
    },
    {
      "category": "Frontend Skills",
      "items": [
        "HTML",
        "CSS",
        "ReactJS",
        "jinja-Templating"
      ]
    },
    {
      "category": "APIs",
      "items": [
        "REST API",
        "Apache Kafka",
        "RabbitMQ",
        "MQTT"
      ]
    },
    {
      "category": "Testing & Debugging",
      "items": [
        "Locust",
        "Postman",
        "Swagger"
      ]
    },
    {
      "category": "Tools & IDEs",
      "items": [
        "Git",
        "GitHub",
        "PyCharm",
        "VS Code",
        "Jupyter Notebook",
        "ArduinoIDE",
        "CUBE IDE",
        "Celery",
        "AWS"
      ]
    },
    {
      "category": "Data Libraries",
      "items": [
        "Pandas",
        "NumPy",
        "LangChain",
        "Requests",
        "Apache AirFlow",
        "ETL"
      ]
    },
    {
      "category": "Methodologies",
      "items": [
        "Agile (Fundamentals)"
      ]
    }
  ],
  "projects": [
    {
      "name": "My Talking Tree (EdTech Product)",
      "technologies": [
        "Python",
        "FastAPI",
        "Express JS",
        "Langchain",
        "Assembly AI",
        "AWS(Polly)",
        "Nginx",
        "AWS(EC2)",
        "OpenAI",
        "Embedded",
        "C",
        "Raspberry PI",
        "NumPy",
        "Unicorn",
        "SQLite",
        "PostgreSQL",
        "Linux",
        "ESP32",
        "BLE",
        "Servo",
        "Raspberry PI"
      ],
      "description": [
        "Developed an AI robotic teacher with advanced facial gestures, including expressive emotions and synchronized mouth movements.",
        "Designed an interactive learning application to engage young pupils in an innovative educational experience."
      ]
    },
    {
      "name": "Magik-mat (EdTech Product)",
      "technologies": [
        "ReactJS",
        "Android studio",
        "express",
        "PostgreSQL",
        "Microservices",
        "Python 3"
      ],
      "description": [
        "Designed Magik Mat as an innovative solution combining education and entertainment to nurture early childhood development.",
        "Developed interactive games that integrate physical activity with engaging educational content for an immersive learning experience."
      ]
    },
    {
      "name": "OKI RG7 & 8TH GENERATION CASH RECYCLERS",
      "technologies": [],
      "description": [
        "Ensured optimal machine performance by updating patches, troubleshooting OS, configuring networks, performing installations, pulling EJ files, and maintaining Solid core connectivity (McAfee)",
        "The 8th generation cash recycler ATM with an advanced Cash Recycler module, building on the legacy of the ATM-Recycler G7's 'Non-stop concept.",
        "Positioned as a pivotal solution for transitioning cash-centric markets and regions to efficient cash recycling"
      ]
    },
    {
      "name": "Verification Lead",
      "technologies": [],
      "description": [
        "Collaborated with esteemed clients such as TVS Credit Sathi, Kotak, Bajaj Auto Finance, and Shriram Chits organizations to deliver client-focused solutions.",
        "Managed loan verifications and approvals for TVS and lead verifications at Kotak.",
        "Oversaw field operations, lead verifications, and claim approvals at Shriram."
      ]
    }
  ],
  "Professional_Summary": "Python Developer with 5+ years of experience in hardware & networking with extensive experience in Python development, utilizing frameworks such as Flask and FastAPI, data analysis with pandas, and proficiency in data structures and algorithms. Skilled in Embedded C programming, HTML with Jinja2 templating and EJS, SQLite, and Bootstrap for front-end development. Experienced in deploying applications on Heroku, testing APIs with Postman, and managing resources on AWS. Competent in Arduino IDE, Node.js, and databases including MongoDB and PostgreSQL. Familiar with EasyEDA for circuit design and experienced in embedded communication protocols such as I2S, SPI, and UART, with expertise in microcontrollers including ESP32, Atmega32, and STM32. Additionally, proficient in message brokers and distributed systems including Kafka, RabbitMQ, Celery, Redis, and MQTT.",
  "Year_of_experience": 5
}




user_info =f"""Candidate Profile : {res_data} \n Missing Keywords : {miskey}"""

print(rebuilt_agent.delay(resume_rebuilt_prompt,user_info))
