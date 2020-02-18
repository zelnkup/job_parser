import time
import csv
import requests
import io
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KABUL, like Gecko) '
                         'Chrome/77.0.3865.120 Safari/537.36'}

base_url = 'https://hh.ru/search/vacancy?clusters=true&area=5&enable_snippets=true&salary=&st=searchVacancy&text=python'


def hh_parse(base_url, headers):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        request = session.get(base_url, headers=headers)
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://hh.ru/search/vacancy?L_is_autosearch=false&area=5&clusters=true&enable_snippets=true' \
                      f'&text=python&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass
        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            divs = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
            for div in divs:
                try:
                    title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                    href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                    company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                    text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                    text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                    content = text1 + ' ' + text2
                    jobs.append({
                        'title': title,
                        'href': href,
                        'company': company,
                        'content': content
                    })
                except:
                    pass
            print(len(jobs))
    else:
        print("ERROR" + str(request.status_code))
    return jobs


def file_writer(jobs):
    with io.open('parsed_jobs.csv', 'w', encoding="utf-8") as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Title', 'URL', 'Company', 'Content'))
        for job in jobs:
            a_pen.writerow((job['title'], job['href'], job['company'], job['content']))

jobs = hh_parse(base_url, headers)
file_writer(jobs)
