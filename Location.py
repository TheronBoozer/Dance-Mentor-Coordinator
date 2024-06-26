import math
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Schedule import Schedule
from Helpers import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

#undetected chromedriver imports
import undetected_chromedriver as uc
from fake_useragent import UserAgent

class Location:
    id = 0     #353 is the dance studio
    schedule = Schedule()
    open_time = 0
    close_time = 0
    name = ""

    def __init__(self, space_id, open_time, close_time):
        self.id = space_id
        self.open_time = open_time * 4
        self.close_time = close_time * 4
        self.set_schedule()

    
    def get_unix_times(self):
        # print("calendar:")
        response = requests.get("https://25live.collegenet.com/25live/data/wpi/run/rm_reservations.ics?caller=pro&space_id={}&start_dt=0&end_dt=+6&options=standard".format(self.id))
        soup = BeautifulSoup(response.text, "html.parser")
        soup.prettify

        cal_text = soup.text
        cal_data = cal_text.split("\n")

        cal_times = []
        for data in cal_data:
            if data.startswith("DTSTART;TZID=America/New_York:"):
                dt = data.removeprefix("DTSTART;TZID=America/New_York:")

            elif data.startswith("DTEND;TZID=America/New_York:"):
                dt = data.removeprefix("DTEND;TZID=America/New_York:")

            else:
                continue
            
            dt = timestamp_to_unix(dt)
            cal_times.append(dt)

        
        # print(cal_times)
        return cal_times


    def set_schedule(self):
        self.schedule.set_calendar_vacancies(self.get_unix_times(), self.open_time, self.close_time)


    def get_name_and_hours(self):
        options = Options()
        # options.add_argument('--headless=new')

        driver = webdriver.Chrome()
        driver.get('https://25live.collegenet.com/pro/wpi#!/home/location/353/details')

        html1 = driver.page_source

        details_page = driver.execute_script("return document.documentElement.innerHTML;")
        
        # details_page = requests.get('https://25live.collegenet.com/pro/wpi#!/home/location/353/details')
        # souper_details = BeautifulSoup(details_page, "html.parser")
        # souper_details.prettify()
        print(details_page)



def setup_driver():
    """
    Sets up a Chromedriver with optimal options for ask_gpt. \
    """

    # grab normal options
    op = webdriver.ChromeOptions()
    # make chrome a random user
    op.add_argument(f"user-agent={UserAgent.random}")
    # give chrome that users data
    op.add_argument("user-data-dir=./")
    # idk what these do
    op.add_experimental_option("detach", True)
    op.add_experimental_option("excludeSwitches", ["enable-logging"])

    # make the driver!
    driver = uc.Chrome(chrome_options=op)


    return driver
