from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import pyautogui
from requests.adapters import HTTPAdapter, Retry
import re


class HTMLProcessor:
    url = ""

    def __init__(self, url=""):
        self.url = url

    def get_genres_from_HTML(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            div_element = soup.find("div", class_="gutter_header pad", string="Browse by genre")
            links = div_element.find_next_siblings("a")
            genre_dict = {}
            for link in links:
                genre_dict[link.text.strip()] = link['href']
            return genre_dict
        else:
            return None

    def get_games_from_HTML(self, genre_link):
        driver = webdriver.Chrome()
        driver.get(genre_link)
        time.sleep(2.5)
        pyautogui.press('end')
        time.sleep(1)
        pyautogui.press('pageup')
        time.sleep(3)
        html_code = driver.page_source
        driver.quit()

        game_links_dict = {}
        soup = BeautifulSoup(html_code, 'html.parser')
        div_element = soup.find("div", class_="NO-IPpXzHDNjw_TLDlIo7")
        div_links = div_element.find_all(class_="StoreSaleWidgetTitle")
        for name in div_links:
            href = name.parent
            app_id_parse = HTMLProcessor(href['href'])
            app_code = app_id_parse.extract_app_id_from_url()
            game_links_dict[name.text] = app_code
        return game_links_dict

    def get_online_num(self, game_id):
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        response = requests.get('https://www.google.com')
        try:
            response = s.get(self.url + game_id)
        except requests.exceptions.ConnectionError:
            print("Connection error. Repeat the request after some time.")
        result = None
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            try:
                div_element = soup.find("span", class_="apphub_NumInApp")
                result = int(div_element.text.split()[0].replace(',', ""))
            except Exception as err:
                print(print(f"Caused error: {err}"))
        return result, response.url

    def extract_app_id_from_url(self):
        match = re.search(r"/app/(\d+)", self.url)
        if match:
            app_id = int(match.group(1))
            return app_id
