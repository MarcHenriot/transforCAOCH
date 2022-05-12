from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

with open('scraper/data/urls.txt', 'w') as f:
    for page in range(1, 57):
        url = f"https://www.allocine.fr/membre-Z20090323193222567627582/critiques/films/?page={page}"

        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, features="html.parser")
        for a in soup.find_all("a", href=True, class_="link-more"):
            f.write("https://www.allocine.fr/membre-Z20090323193222567627582/critiques/" + a["href"].split('/')[-2] + "\n")
    
    browser.close()

