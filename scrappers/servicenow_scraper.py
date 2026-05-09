import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

companyName = "ServiceNow"
jobType = "NA"

# url = "https://careers.servicenow.com/jobs/?search=&origin=global"
baseurl = "https://careers.servicenow.com"
url = f"{baseurl}/jobs"
resJobList = requests.get(url)
soupJobList = BeautifulSoup(resJobList.text,"html.parser")

jobs = soupJobList.find("div",id="js-job-search-results").find_all("div",class_="card card-job")

with open("../csv_files/servicenow_jobs.csv","w",newline="",encoding="utf-8") as file:
    writer = csv.writer(file)

    # Header row
    writer.writerow(["job_name","job_desc","posting_date","location","company_name","job_type","job_application_link"])

    for job in jobs:
        jobLink = job.find("a")
        jobName = jobLink.text.strip()
        jobDescLink = f"{baseurl}{jobLink.get("href")}"
        location = job.find("ul").text.strip()
        # print(jobDescLink)

        resJobDetails = requests.get(jobDescLink)
        soupJobDetails = BeautifulSoup(resJobDetails.text,"html.parser")

        jobInfo = soupJobDetails.find("section",class_="hero-job").find_all("li")
        for info in jobInfo:
            svgname = info.find("use").get("xlink:href").split("#")[-1]
            if svgname=="remote":
                jobType = info.text.strip()
            
        postingDate = soupJobDetails.find("section",class_="hero-job").find("time").get("datetime")
        fomattedPostingDate = datetime.strptime(postingDate,"%Y-%m-%d").strftime("%d-%m-%Y")
        
        applyLink = soupJobDetails.find("a",id="js-apply-external").get("href")
        jobDesc = soupJobDetails.find("article",class_="cms-content").get_text("",strip=True)

        writer.writerow([jobName,jobDesc,fomattedPostingDate,location,companyName,jobType,applyLink])
    
print("saved in csv")


