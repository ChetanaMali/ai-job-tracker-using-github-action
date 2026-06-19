import requests
import os


APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")


country = "in"

url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"


params = {

    "app_id": APP_ID,
    "app_key": APP_KEY,

    "results_per_page": 20,

    "what":
    "DevOps Engineer OR Cloud Engineer",

    "where":
    "India"
}


response = requests.get(
    url,
    params=params
)


data = response.json()


jobs = data["results"]


keywords = [
    "aws",
    "docker",
    "kubernetes",
    "jenkins",
    "terraform",
    "linux"
]


matches = []


for job in jobs:

    text = (
        job.get("title","")
        +
        job.get("description","")
    ).lower()


    score = 0


    for k in keywords:
        if k in text:
            score += 1


    if score >= 2:

        matches.append({

            "title":
            job["title"],

            "company":
            job["company"]["display_name"],

            "location":
            job["location"]["display_name"],

            "score":
            score,

            "url":
            job["redirect_url"]
        })


print("\nTOP DEVOPS JOBS\n")


for job in matches[:5]:

    print("----------------")
    print("Role:",job["title"])
    print("Company:",job["company"])
    print("Location:",job["location"])
    print("Match:",job["score"],"/10")
    print("Apply:",job["url"])