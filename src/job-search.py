from datetime import datetime


print("Job Tracker Started")

print(
f"""
Date:
{datetime.now()}

Searching jobs...
"""
)


jobs = [
    {
        "role":"Cloud Engineer Intern",
        "company":"Example Company",
        "skills":"AWS Docker Linux"
    },

    {
        "role":"DevOps Engineer Fresher",
        "company":"Example Startup",
        "skills":"Jenkins Kubernetes AWS"
    }
]


for job in jobs:
    print("----------------")
    print(job["role"])
    print(job["company"])
    print(job["skills"])