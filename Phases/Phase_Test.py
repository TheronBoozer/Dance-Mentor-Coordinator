import os
import requests
from bs4 import BeautifulSoup

from Globals.Helpers import create_2d_array, get_links, save_object, recycle_object
from Globals.file_paths import PICKLE_TEST, TEST_OUTLINE
from Objects.Location import Location
from Objects.Mentor import Mentor


def test():
    with open(TEST_OUTLINE, 'r') as text:
        statement = text.read()

    # General Tests
    statement = statement.replace("[OS]", get_os())
    statement = statement.replace("[CRONTAB]", cron_check())
    statement = statement.replace("[WIFI]", get_wifi())
    statement = statement.replace("[LINK]", test_links())
    statement = statement.replace("[PICKLES]", test_pickles())


    # Scrape Tests
    statement = statement.replace("[LOCATION]", test_location())
    statement = statement.replace("[MENTOR]", test_mentor())
    statement = statement.replace("[SESSION]", test_session())
        
    print(statement)


def get_os() -> str:
    operating_sys = os.name
    if operating_sys == 'nt':
        return "Windows"
    elif operating_sys == 'posix':
        return "Linux"
    else:
        return "Who the fuck knows"

def cron_check() -> str:
    term = os.getenv("TERM")
    display = os.getenv("DISPLAY")

    if term == None and display == None:
        return green("Run through Crontab")
    else:
        return red("Not run through Crontab")

def get_wifi():
    try:
        requests.get("https://google.com", timeout=5)
        return green("Connected to the Internet")
    except Exception as e:
        return red("Failed to connect to the internet", repr(e))

def test_links() -> str:
    try:
        get_links()
        return green("Links Accessed")
    except Exception as e:
        return red("Links Unaccessible", repr(e))
    
def test_pickles():
    try:
        save_object("Pickling Functional", PICKLE_TEST)
        fin = recycle_object(PICKLE_TEST)
        return green(fin)
    except Exception as e:
        return red("Pickling failed", repr(e))
    
    

def test_location() -> str:
    try:
        location_sheet = get_links["LOCATION_INFORMATION_SHEET_LINK"]                 # fetch the location sheet link
        location_information = create_2d_array(location_sheet)                          # make a 2d array of the location information
        Location(location_information[0])
        fin = f"{len(location_information)} locations found"
        return green(fin)
    except Exception as e:
        return red("Locations not found", repr(e))
    
def test_mentor() -> str:
    try:
        mentor_sheet = get_links["MENTOR_INFORMATION_SHEET_LINK"]                 # fetch the location sheet link
        mentor_information = create_2d_array(mentor_sheet)                          # make a 2d array of the location information
        Mentor(mentor_information[0])
        fin = f"{len(mentor_information)} mentors found"
        return green(fin)
    except Exception as e:
        return red("Mentors not found", repr(e))
    
def test_session() -> str:
    try:
        session_sheet = get_links["SESSION_INFORMATION_SHEET_LINK"]                 # fetch the location sheet link
        session_information = create_2d_array(session_sheet)                          # make a 2d array of the location information
        Location(session_information[0])
        fin = f"{len(session_information)} sessions found"
        return green(fin)
    except Exception as e:
        return red("Sessions not found", repr(e))







def red(skk : str, error=None) -> str: 
    if error == None:
        return '<p style="color: red;">{}</p>' .format(skk)
    else:
        return '<p style="color: red;">{}, failed with error:<br>{}</p>' .format(skk, error)
 
 
def green(skk : str) -> str: 
    return('<p style="color: green;">{}</p>' .format(skk))
