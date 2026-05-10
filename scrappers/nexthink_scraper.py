import requests
import pandas as pd
from datetime import datetime, timedelta, timezone

url = "https://api.smartrecruiters.com/v1/companies/Nexthink/postings"

resJobList = requests.get(url)

jobData = resJobList.json()
# print(data['content'])

# job_name company_name posting_date location job_application_link

jobs = []
now = datetime.now(timezone.utc)
two_days_ago = now - timedelta(days=2)
jobType = "NA"

for job in jobData['content']:
    releasedDate = datetime.fromisoformat(job.get("releasedDate").replace("Z", "+00:00"))

    if releasedDate >= two_days_ago:
        jobName = job.get("name")
        companyName = job.get("company").get("name")
        postingDate = releasedDate.strftime("%d-%m-%Y")
        location = job.get("location").get("fullLocation")

        isRemote = job.get("location").get("remote")
        isHybrid = job.get("location").get("hybrid")
        
        jobDescLink = job.get("ref")
        
        if isRemote:
            jobType = "Remote"
        elif isHybrid:
            jobType = "Hybrid"
        
        resJobDetails = requests.get(jobDescLink)
        jobDetailsData = resJobDetails.json()

        # print(isRemote,isHybrid,jobType)

        jobs.append({
            "job_name": jobName,
            "job_desc": jobDetailsData.get("jobAd"),
            "posting_date": postingDate,
            "location": location,
            "company_name": companyName,
            "job_type": jobType,
            "job_application_link": jobDetailsData.get("applyUrl"),
        })

# print(jobs)

df = pd.DataFrame(jobs)

print(df.head())

df.to_csv("../csv_files/nexthink_jobs.csv", index=False)