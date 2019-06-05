import os
import sys
import pandas as pd
import numpy as np
import json
import time
import datetime
import requests
import pickle
import subprocess
from bs4 import BeautifulSoup

api_key = 'bJ8ItrrWok5LoEwRH79cOpukP0PndafC'

def get_all_articles(articles):
    years_num = list(np.arange(1981,2019))
    years = []

    for year in years_num:
        years.append(str(year))

    months_num = list(np.arange(1,13))
    months = []
    daysIn = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for month in months_num:
        months.append(str(month))
    for year in years:
        articles[year] = {}
        for month in months:
            if year == '2019' and month == '5':
                break
            articles[year][month] = {}
            print('Getting {}/{} articles'.format(year,month))
            #url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
            url = 'https://api.nytimes.com/svc/archive/v1/{}/{}.json'.format(year,month)

            # begin = ""
            # if len(month) == 1:
            #     month = "0" + month
            # begin += year + month + "01"
            # endDay = str(daysIn[int(month) - 1])
            # end = year + month + endDay




            #params = {'begin_date': begin, 'end_date': end ,'api-key': api_key}
            params = {'api-key': api_key}
            response = requests.get(url, params=params)
            print(response)

            while response.status_code != 200:
                print('trying again...')
                time.sleep(3)
                response = requests.get(url, params=params)
                print('status code: {}'.format(response.status_code))

            articlesjson = json.loads(response.text)
            print(articlesjson)
            return
            docs = articlesjson['response']['docs']

            articles[year][month] = len(docs)

        print('Dumping year {}.'.format(year))

        with open('archive_export.json', 'w') as fp:
            json.dump(articles, fp)

    print('Exporting articles 1981_1-2018_2 to json')
    with open('archive_export.json', 'w') as fp:
        json.dump(articles, fp)


def get_metadata():
    begin_dates = [20000101, 20010101, 20020101]
    end_dates = [20001231, 20011231, 20021231]
    begin_date = 19930101
    end_date = 19931231
    index = 1
    articles = {}
    exportno = 5
    page = 1

    while page < 101 and exportno < 50 and index <= 3:
        response = None
        if len(articles)>=1000:
            print('Exporting results till page {} to json {}'.format(page-1,exportno))
            with open('metadata_export{}.json'.format(exportno), 'w') as fp:
                json.dump(articles, fp)
            articles = {}
            exportno += 1


#         print('Getting articles from page {}'.format(page))

        #Foreign, Business
        url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
        news = "section_name:(\"Your Money\" \"Job Market\" \"Business\" \"World\" \"Business Day\" \"Technology\") AND document_type:(\"article\") AND type_of_material:(\"news\")"

        tokens = "Job Market"
        params = {'api-key': api_key,
                  'begin_date': begin_date,
                  'end_date': end_date,
                  'fq': news,
                  'page': page}

        while response == None:
            try:
                response = requests.get(url, params=params)
                break
            except requests.exceptions.ConnectionError:
                time.sleep(5)
                continue


#         print('status code: {}'.format(response.status_code))

        time.sleep(0.6)
        temp = False
        while temp or response.status_code != 200:
            print('trying again...')
            time.sleep(3)
            try:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    break
            except requests.exceptions.ConnectionError:
                temp = True
                continue

        articlesjson = json.loads(response.text)

        docs = articlesjson['response']['docs']

        try:
            for i in range(0,len(docs)):
                item = docs[i]

                # Get URL
                articles[item['web_url']] = {}

                # Get Name of Writer
                try:
                    articles[item['web_url']]['writer_name'] = item['byline']['person'][0]['firstname']+' '+item['byline']['person'][0]['lastname']
                except:
                    articles[item['web_url']]['writer_name'] = None

                # Get Publication Date
                try:
                    articles[item['web_url']]['pub_date'] = item['pub_date'][:10]
                    tempdate = ''.join((item['pub_date'][:10]).split('-'))
                except:
                    articles[item['web_url']]['pub_date'] = None

                # Get Snippet
                try:
                    articles[item['web_url']]['snippet'] = item['snippet']
                except:
                    articles[item['web_url']]['snippet'] = None

                # Get Word Count
                try:
                    articles[item['web_url']]['word_count'] = item['word_count']
                except:
                    articles[item['web_url']]['word_count'] = None

                 # Get Score
                try:
                    articles[item['web_url']]['score'] = item['score']
                except:
                    articles[item['web_url']]['score'] = None

                # Get Source
                try:
                    articles[item['web_url']]['source'] = item['source']
                except:
                    articles[item['web_url']]['source'] = None

                # Get Section Name
                try:
                    articles[item['web_url']]['section_name'] = item['section_name']
                except:
                    articles[item['web_url']]['section_name'] = None

                # Get Type of Material
                try:
                    articles[item['web_url']]['type_of_material'] = item['type_of_material']
                except:
                    articles[item['web_url']]['type_of_material'] = None

                # Get Document Type
                try:
                    articles[item['web_url']]['document_type'] = item['document_type']
                except:
                    articles[item['web_url']]['document_type'] = None

                # Get Main / Web Headline
                try:
                    articles[item['web_url']]['main_headline'] = item['headline']['main']
                except:
                    articles[item['web_url']]['main_headline'] = None

                # Get Print Headline
                try:
                    articles[item['web_url']]['print_headline'] = item['headline']['print_headline']
                except:
                    articles[item['web_url']]['print_headline'] = None

            page += 1

            if page%10==0 and page>0:
                print('Get articles page {} success'.format(page))

        except Exception as e:
            print('ERROR:, {}'.format(e))
            return {}

        # if page == 200:
        #     end_date = end_dates[index]
        #     begin_date = begin_dates[index]
        #     index += 1
        #     page = 0
        #     break

    print('Exporting remainder including page {} to json {}'.format(page,exportno))
    with open('metadata_export{}.json'.format(exportno), 'w') as fp:
        json.dump(articles, fp)
def get_bodytext():
    #arr = ["metadata_1981_2", "metadata_1982_1", "metadata_1982_2", "metadata_1982_3", "metadata_1983_1", "metadata_1983_2", "metadata_1983_3", "metadata_1984_1", "metadata_1984_2", "metadata_1984_3", "metadata_1985_1", "metadata_1985_2", "metadata_1986_1", "metadata_1986_2", "metadata_1986_3", "metadata_1987_1", "metadata_1987_2", "metadata_1987_3", "metadata_1988_1", "metadata_1988_2", "metadata_1988_3", "metadata_1989_1", "metadata_1989_2", "metadata_1989_3", "metadata_1990_1", "metadata_1990_2", "metadata_1990_3", "metadata_1991_1", "metadata_1991_2", "metadata_1992_1", "metadata_1992_2", "metadata_1993_1", "metadata_1993_2", "metadata_1994_1", "metadata_1994_2", "metadata_1995_1", "metadata_1995_2", "metadata_1996_1", "metadata_1996_2", "metadata_1997_1", "metadata_1997_2", "metadata_1998_1", "metadata_1998_2", "metadata_1999_1", "metadata_1999_2", "metadata_2000_1", "metadata_2000_2", "metadata_2001_1", "metadata_2001_2", "metadata_2002_1", "metadata_2002_2"]
    arr = ["metadata_2017_1", "metadata_2017_2", "metadata_2018_1", "metadata_2018_2"]
    i = 0
    for file in arr:
        name = "Temp/"
        name += file
        name += ".json"
        with open(name) as fp:
            articles = json.load(fp)

        for url in articles.keys():
            print(i)
            i += 1
#             print(url)
            page = None
            while page == None:
                try:
                    #page = requests.get(url, timeout=9)
                    page = requests.get(url)
                    break
                except requests.exceptions.ConnectionError:
                    time.sleep(5)
                    continue
                except requests.exceptions.Timeout:
                    print("not good")
                    time.sleep(45)
                    continue

#             time.sleep(0.2)
            soup = BeautifulSoup(page.text, 'lxml')
            text = soup.findAll(attrs={'class':'story-body-text story-content'})
            if text == []:
                text = soup.findAll(attrs={'class':'story-body-text'})
            if text == []:
                text = soup.findAll(attrs={'itemprop':'articleBody'})
            if text == []:
                text = soup.findAll(attrs={'itemprop':'reviewBody'})
            body_text = ''
            for paragraph in text:
                body_text += (' **********'+paragraph.get_text())
            articles[url]['body_text'] = body_text



#             time.sleep(0.6)
        # Write to .json
        print('{}: exporting to bodytext_export{}.json'.format(datetime.datetime.now(),i))
        output = "FullOutput/"
        output += file[9:]
        output += "_fulltext"
        output += ".json"
        with open(output, 'w') as fp:
            json.dump(articles, fp)

    print("end")
    print(i)
    print("articles")

if 'darwin' in sys.platform:
    print('Running \'caffeinate\' on MacOSX to prevent the system from sleeping')
    subprocess.Popen('caffeinate')
#get_metadata()
get_bodytext()
#get_all_articles(articles)




