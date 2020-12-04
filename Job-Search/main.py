import requests
import bs4
from bs4 import BeautifulSoup

import pandas as pd
import time

def URLGen(country, job, location):
    URL_Job = "+".join(job.split())
    URL_Location = "+".join(location.split())
    
    #Checks if correct input
    if country == 'Yes' or 'yes':
        URL = "https://www.indeed.com/jobs?q="+str(URL_Job)+"+24"+"%2C000&l="+str(URL_Location)
    else:
        print("sorry we only offer options for people in the US.")
        URL = ''

    return(URL)

def job_title_result(soup):
    #Create Empty list for jobs
    jobs = []
    for div in soup.find_all(name="div",attrs={"class":"row"}):
        for a in div.find_all(name="a",attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"]) #Search through elements of website that have job title and put it in the lsit
    return(jobs)

def location_result(soup):
    locations = []
    spans = soup.find_all("span", attrs={"class": "location"})
    for span in spans:
        locations.append(span.text)
    return(locations)


def summary_result(soup):
    summaries = []
    spans = soup.find_all("span", attrs={"class":"summary"})
    for span in spans:
        summaries.append(span.text.strip())
    return(summaries)

def findJobs(URL):
    if URL != '':
        #Get URL from requests
        page = requests.get(URL)
        soup = BeautifulSoup(page.text, "html.parser")
        
            
        jobs = job_title_result(soup)
        locations = location_result(soup)
        
        # print the final string

        string_final = '%-10s%-60s%s'
        # print(string_final % ('', 'Job title', 'Location', 'salary'))
        for i, (job, location) in enumerate(zip(jobs, locations)):
            print(string_final % (i, job, location))

def PageGen(URL):
    pageUrls = []
    for x in range(10, 40, 10):
        pageUrls.append(URL+"&start="+str(x))
    return pageUrls

#User inputs
country = input("Do you live in the US?: ")
job = input("type of job you're looking for: ")
location = input("What state do you live in: ")

#Generate URL
URL = URLGen(country, job, location)

#grab page Urls
pageUrls = PageGen(URL)

x = 1
#Loop through the list of pageURLS
string_final = '%-10s%-60s%s'
print(string_final % ('', 'Job title', 'Location'))
for page in pageUrls:
    print("Page "+str(x))
    findJobs(page)
    x = x + 1
