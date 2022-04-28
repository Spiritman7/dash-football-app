from numpy import source
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests
import json
from transformers import pipeline
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
from time import sleep
import asyncio
import sys
import pandas as pd
import os
from dotenv import load_dotenv



load_dotenv()

DRIVER_PATH = os.getenv("DRIVER_PATH")
CHROME_PATH = os.getenv("CHROME_PATH")



# Establish locations of driver and browser
driver_path = DRIVER_PATH
chrome_path = CHROME_PATH
service = Service(driver_path)



# Utilize Chrome Driver for automation purposes (initiate Chrome driver)
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument('--headless')    # browser will not pop up while running
browser = webdriver.Chrome(service=service, options=options)



"""  Get latest news of teams from top 5 regions in UK 

1. Manchester
2. Liverpool
3. Chelsea
4. Arsenal 

  """

source_link_1 = "https://www.manchestereveningnews.co.uk/sport/football/"
source_link_2 = "https://www.liverpoolecho.co.uk/sport/football/football-news/"
source_link_3 = "https://www.thechelseachronicle.com/"
source_link_4 = "https://www.arsenal.com/news?field_article_arsenal_team_value=men&revision_information="



# Summarize articles linked to Manchester teams  
def get_manchester_summary():
    team = 'Manchester teams'
    browser.get(source_link_1)  
    link_element = browser.find_element(By.TAG_NAME, 'a.headline')
    url = link_element.get_attribute('href')

    print('Loading summarizer from Transformers.........')
    summarizer = pipeline("summarization")
    print('Summarizer loaded successfully')
    time.sleep(3)



    print(f'Now scraping webpage for {team} ... ')
    link = url
    response = requests.get(link).text

    print(f'Now parsing content from HTML elements...')
    soup = BeautifulSoup(response, 'html.parser')
    results = soup.find_all(['h1', 'p'])
    text = [result.text for result in results]
    article = ' '.join(text)
    article = article.replace('.', '.<--------->')
    article = article.replace('?', '?<--------->')
    article = article.replace('!', '!<--------->')
    sentences = article.split('<--------->')
    current_chunk = 0
    chunks = [] 
    max_chunk = 500


    print('------------------------------------')
    print('Now splitting sentences into smaller units for pre-processing...')
    for sentence in sentences:
        if len(chunks) == current_chunk + 1: 
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            print(current_chunk)
            chunks.append(sentence.split(' '))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])
    

    
    print('------------------------------------')
    print('Loading final summary.....')


    results = summarizer(chunks, min_length=50, max_length=150, do_sample=False)
    results_df = pd.DataFrame(results)
    results_df_2 = results_df['summary_text'].apply(pd.Series)
    output = results_df_2.explode(0).assign(Co2 = lambda x: x[0].str.get('rank')).reset_index(drop=True)
    final_summary = output[0]
    
    print("---------------")
    print("Here's your football summary:")
    print(final_summary[3])
    print("---------------")
    # browser.close()
    browser.quit()

    return final_summary[3]



get_manchester_summary()