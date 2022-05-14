import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def clean_meta(txt):
    txt = txt.split('\n')[-4:-1]
    txt = ' '.join(txt)
    txt = txt.split('/')[-1].strip()
    return txt

def clean_director(txt):
    txt = txt.split('\n')[-2]
    return txt

def clean_cast(txt):
    txt = txt.split('\n')[-4:-1]
    txt = ' '.join(txt)
    return txt

data = pd.read_csv('data/data.csv')

for line in data.iterrows():
    film_id = line[1]['id']
    url = f"https://www.allocine.fr/film/fichefilm_gen_cfilm={film_id}.html"
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
    
    title = soup.find("div", class_="titlebar-title-lg").text
    meta = clean_meta(soup.find("div", class_="meta-body-info").text)
    director = clean_director(soup.find("div", class_="meta-body-direction").text)
    cast = clean_cast(soup.find("div", class_="meta-body-actor").text)

    data.loc[data['id'] == film_id, 'title'] = title
    data.loc[data['id'] == film_id, 'meta'] = meta
    data.loc[data['id'] == film_id, 'director'] = director
    data.loc[data['id'] == film_id, 'cast'] = cast

    browser.close()

    data.to_csv('data/data_v2.csv', index=False)