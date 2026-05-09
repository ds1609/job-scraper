import requests
from bs4 import BeautifulSoup
import csv

url = "https://apply.deloitte.com/en_US/careers/SearchJobs/SFL%20Scientific?sort=relevancy"
resJobList = requests.get(url)
soupJobList = BeautifulSoup(resJobList.text,"html.parser")

jobs = soupJobList.find_all("article",class_="article--result")

jobName = ""
jobDesc = ""
postingDate = "NA"
companyName = ""
jobType = "NA"
applyLink = ""

with open("../csv_files/sfl_jobs.csv","w",newline="",encoding="utf-8") as file:
    writer = csv.writer(file)

    # Header row
    writer.writerow(["job_name","job_desc","posting_date","location","company_name","job_type","job_application_link"])

    for job in jobs:
        jobLink = job.find("a",class_="link")
        jobName = jobLink.text.strip()
        companyName = job.find("div",class_="article__header__text__subtitle").find("span").text.strip()
        jobDescLink = jobLink.get("href")

        resJobDetails = requests.get(jobDescLink)
        soupJobDetails = BeautifulSoup(resJobDetails.text,"html.parser")

        jobLocations = soupJobDetails.find("div",class_="article__header--locations").find_all("p",class_="paragraph")
        # print(jobLocations)
        locations = []
        for loc in jobLocations:
            # print(loc.text)
            locations.append(loc.text)

        locationStr = "|".join(locations)
        applyLink = soupJobDetails.find("div",class_="button-bar button-bar--1col").find("a").get("href")

        
        # jobDesc = soupJobDetails.find("div",class_="article__view")
        jobDesc = soupJobDetails.find("div",class_="article__view").get_text("",strip=True)
        # print(jobDesc)

        # print(jobName,companyName,",".join(locations),applyLink)
        writer.writerow([jobName,jobDesc,postingDate,locationStr,companyName,jobType,applyLink])

print("saved in csv")




