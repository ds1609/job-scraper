import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

companyName = "Tech Mahindra"
jobType = "NA"

url="https://careers.techmahindra.com/"
resJobList = requests.get(url)
# print(resJobList.text)
soupJobList = BeautifulSoup(resJobList.text,"html.parser")
# print(soupJobList)
jobs = soupJobList.find("div",class_="joblisting").find_all("div",class_="title2")

with open("../csv_files/techmahindra_jobs.csv","w",newline="",encoding="utf-8") as file:
    writer = csv.writer(file)

    # Header row
    writer.writerow(["job_name","job_desc","posting_date","location","company_name","job_type","job_application_link"])

    for job in jobs:
        jobName = job.find("div").find("div").text
        jobDescLink = f"{url}{job.find("div").find("a").get("href")}"
        # print(jobDescLink)
        applyLink = jobDescLink

        resJobDetails = requests.get(jobDescLink)
        soupJobDetails = BeautifulSoup(resJobDetails.text,"html.parser")
        # print(soupJobDetails.prettify())

        jobDetailsDiv = soupJobDetails.find("div",id="ctl00_ContentPlaceHolder1_JDSetion").find_all("div")
        jobDetails = jobDetailsDiv[0].find_all("li")
        postingDate = jobDetails[3].find("span").text.strip()
        # fomattedPostingDate = datetime.strptime(postingDate,"%d/%m/%Y").strftime("%d-%m-%Y")
        location = jobDetails[6].find("span").text.strip()
        # print(postingDate,location)

        jobDesc = jobDetailsDiv[2].text.strip()
        # print(jobDesc)

        writer.writerow([jobName,jobDesc,postingDate,location,companyName,jobType,applyLink])
    
print("saved in csv")

