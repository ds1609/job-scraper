import requests
import pandas as pd
import json
import re
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup

baseurl = "https://issgovernance.wd1.myworkdayjobs.com/wday/cxs/issgovernance/ISScareers"
# url = "https://issgovernance.wd1.myworkdayjobs.com/wday/cxs/issgovernance/ISScareers/jobs"
url = f"{baseurl}/jobs"

# print(url)
payload = {
    "appliedFacets": {},
    "limit": 20,
    "offset": 0,
    "searchText": ""
}

headers = {
    "Content-Type": "application/json"
}

resJobList = requests.post(url, json=payload, headers=headers)

jobData = resJobList.json()
# print(json.dumps(jobData, indent=2))

jobs = []
days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
jobType = "NA"

for job in jobData["jobPostings"]:
    postedOn = job.get("postedOn")
    # Extract number
    days = int(re.search(r"\d+", postedOn).group())
    # Get actual date
    postingDate = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    fomattedPostingDate = datetime.strptime(postingDate,"%Y-%m-%d").strftime("%d-%m-%Y")
    # print(postingDate, days_ago)

    if postingDate >= days_ago:
        jobName = job.get("title")
        location = job.get("locationsText")
        # jobDescLink = f"{baseurl}/en-US/ISScareers{job.get("externalPath")}"
        jobDescLink = f"{baseurl}{job.get("externalPath")}"
        # print(jobName,jobDescLink)

        resJobDetails = requests.get(jobDescLink)
        jobDetailsData = resJobDetails.json()
        # print(json.dumps(jobDetailsData, indent=2))

        companyName = jobDetailsData.get("hiringOrganization").get("name")
        jobDescData = jobDetailsData.get("jobPostingInfo").get("jobDescription")
        applyLink = jobDetailsData.get("jobPostingInfo").get("externalUrl")

        soupJobDetails = BeautifulSoup(jobDescData,"html.parser")
        jobDesc = soupJobDetails.text.strip()
        
        jobs.append({
            "job_name": jobName,
            "job_desc": jobDesc,
            "posting_date": fomattedPostingDate,
            "location": location,
            "company_name": companyName,
            "job_type": jobType,
            "job_application_link": applyLink,
        })

df = pd.DataFrame(jobs)

# print(df.head())

df.to_csv("../csv_files/iss_jobs.csv", index=False)
