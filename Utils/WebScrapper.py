import requests
from bs4 import BeautifulSoup

class WebScrapper:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

    def get_html_markup(self,url):
        page = requests.get(url).text
        soup_markup = BeautifulSoup(page, 'html.parser')
        return soup_markup

    def get_html_markup_with_header(self,url):
        page = requests.get(url, headers=self.headers).text
        soup_markup = BeautifulSoup(page, 'html.parser')
        return soup_markup