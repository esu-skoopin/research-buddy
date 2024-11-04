import time

from bs4 import BeautifulSoup
import requests

import json

def grab_links_per_subject(subjects, links=[]):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://arxiv.org/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    arXiv = requests.get('https://arxiv.org/', headers=headers)
    soup = BeautifulSoup(arXiv.text, 'html.parser')
    time.sleep(10)

    i = 0
    subList = list(subjects.keys())
    currSubject = subList[i]

    currCount = subjects[currSubject]
    count = 0

    for a in soup.find_all('a', href=True, id=lambda x: x and x.startswith('main-')):
        if count == currCount:
            subjects[currSubject] = links
            links = []
            count = 0
            i += 1
            currSubject = subList[i]
            currCount = subjects[currSubject]

        if currSubject == 'Computer Science':
            a['href'] = "/archive/cs"

        count += 1
        url = 'https://arxiv.org' + a['href']
        links.append(url)

    subjects[currSubject] = links

    return subjects

def year_range_per_topic(subjects, years=[]):
    res = {}

    for subject, urls in subjects.items():
        for curr in urls:
            res[curr] = 0
            archive = requests.get(curr)
            soup = BeautifulSoup(archive.text, 'html.parser')

            for a in soup.find_all('a', href=lambda x: x and x.startswith('/year/')):
                if a.get_text():
                    years.append(a.get_text())

            res[curr] = (years[0], years[-1])
            years = []
    return res

def grab_count_per_year(topic_to_range):

    for topic, range in topic_to_range.items():
        start = int(range[0])
        end = int(range[1])

        count_list = []
        while start >= end:
            currCount = []
            topic_name = topic.split('/')[-1]
            url = 'https://arxiv.org/year/' + topic_name + '/' + str(start)
            stats = requests.get(url)
            soup = BeautifulSoup(stats.text, 'html.parser')

            for count, b in enumerate(soup.find_all('b')):
                if b.get_text().isdigit() and int(b.get_text()) > 0:
                    curr = f"{count:.2f}"
                    currCount.append(curr)

            count_list.append(currCount)
            start -= 1
        topic_to_range[topic] += (count_list,)

subjects = {
    "Physics": 13,
    "Mathematics": 1,
    "Computer Science": 1,
    "Quantitative Biology": 1,
    "Quantitative Finance": 1,
    "Statistics": 1,
    "Electrical Engineering and Systems Science": 1,
    "Economics": 1}

# Grabs every topic URL per subject
grab_links_per_subject(subjects)
print(subjects)
# Using the URLs, we grab the start and end range of each topic
topic_to_range = year_range_per_topic(subjects)
# Now we will append the count of
grab_count_per_year(topic_to_range)
print(topic_to_range)
