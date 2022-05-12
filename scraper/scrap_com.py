from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re

def clean_txt(txt):
    txt = txt.replace('\n', ' ')
    txt = txt.replace('\t', ' ')
    txt = txt.replace('\r', ' ')
    txt = re.sub(' +', ' ', txt)
    txt = txt.strip()
    return txt


if __name__ == '__main__':
    data = {
        'id': [],
        'comment': [],
    }
    with open('scraper/data/urls.txt', 'r') as f:
        urls = f.readlines()
        for url in urls:
            browser = webdriver.Chrome(ChromeDriverManager().install())
            browser.get(url)
            html = browser.page_source
            soup = BeautifulSoup(html, features="html.parser")
            
            comment = soup.find("div", class_="review-card-content").text.strip()
            id_ = int(url.split("/")[-2].split("-")[-1])
            
            data['id'].append(id_)
            data['comment'].append(clean_txt(comment))

            df = pd.DataFrame.from_dict(data)
            df.to_csv('scraper/data/data.csv', index=False)
        
        browser.close()