import requests
import os
#Gemini API
from google import genai
#Gmail API
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
##### AI ANALYSIS FUNCTION ######
def analyze_job(job):

    resume = open(
        "src/resume.txt"
    ).read()


    prompt = f"""

You are a recruiter hiring freshers for Cloud and DevOps roles.

Candidate is:
- Fresher
- 0 years experience
- Looking for entry-level DevOps/Cloud roles

Prefer:
- DevOps Intern
- Junior DevOps Engineer
- Cloud Support Engineer
- Cloud Engineer Trainee

Do not recommend senior roles.

Analyze this job and return ONLY this format:

Job Name:
Company Name:
Address/Location:
Experience Required:
Apply Link:
Required Skills:
Match Score:
Should Apply: YES/NO

Candidate Resume:

{resume}


Job Details:

Role:
{job['title']}

Company:
{job['company']}

Location:
{job['location']}

Experience Required:
{job.get('description','')}


STRICT RULE:
Only recommend jobs requiring:
- 0 years experience
- Fresher
- 0-1 years experience

Reject:
- 2+ years
- Senior
- Lead
- Experienced roles



"""


    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text

####### EMAIL FUNCTION ######

def send_email(content):

    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_TO")


    msg = MIMEMultipart()

    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "Daily DevOps Job Alert"


    msg.attach(
        MIMEText(
            content,
            "plain"
        )
    )


    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        sender,
        password
    )


    server.sendmail(
        sender,
        receiver,
        msg.as_string()
    )

    server.quit()


country = "in"

url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"


params = {

    "app_id": APP_ID,
    "app_key": APP_KEY,

    "results_per_page": 50,

    "what":
    "DevOps Engineer",

    "where":
    "India",

    "max_days_old": 10

}


response = requests.get(
    url,
    params=params
)


data = response.json()

print(data)

jobs = data["results"]


keywords = [
    "aws",
    "docker",
    "kubernetes",
    "jenkins",
    "terraform",
    "linux",
    "anisible",
    "cloud"
]

experience_keywords = [
    "fresher",
    "0-1 year",
    "0 years",
    "1 year",
    "junior",
    "intern",
    "entry level",
    "graduate"
]
experience_block = [
    "2 years",
    "3 years",
    "4 years",
    "5 years",
    "6 years",
    "7 years",
    "8 years",
    "10 years",
    "minimum 2",
    "minimum 3",
    "minimum 5",
    "experience required: 2",
    "experience required: 3",
    "experience required: 5"
]
senior_keywords = [
    "senior",
    "lead",
    "architect",
    "manager",
    "5 years",
    "7 years",
    "10 years"
]
fresher_bonus = [
    "intern",
    "trainee",
    "junior",
    "entry",
    "graduate",
    "fresher",
    "0-1"
]
matches = []

jobs = data["results"]
print("Total jobs from Adzuna:", len(jobs))

for job in jobs:
    print(
        "\nJOB:",
        job.get("title"),
    )
    text = (
        job.get("title","")
        +
        job.get("description","")
    ).lower()

    # Remove jobs needing more than 1 year experience

    if any(word in text for word in experience_block):
        continue

    score = 0


    for k in keywords:
        if k in text:
            score += 1

    for k in experience_keywords:
        if k in text:
            score += 3

    for k in senior_keywords:
        if k in text:
            score -= 5
    for k in fresher_bonus:
        if k in text:
            score += 5

    print("Score:", score)

    if score >= 2:

        


        matches.append({

            "title":
            job["title"],

            "company":
            job["company"]["display_name"],

            "location":
            job["location"]["display_name"],
            
            "description": job.get("description",""),

            "score":
            score,

            "url":
            job["redirect_url"]
        })


print("\nTOP DEVOPS JOBS\n")

email_body = ""


for job in matches[:5]:

    print("----------------")
    print("Role:",job["title"])
    print("Company:",job["company"])
    print("Location:",job["location"])
    print("Match:",job["score"],"/10")
    print("Apply:",job["url"])

    try:

        analysis = analyze_job(job)

    except Exception as e:

        analysis = "AI analysis failed: " + str(e)


    print("\nAI Analysis:")
    print(analysis)
    email_body += f"""

    ======================

    Job:
    {job['title']}

    Company:
    {job['company']}

    Location:
    {job['location']}

    Apply:
    {job['url']}

    AI Analysis:

    {analysis}

    """

send_email(email_body)

print("Email sent successfully")