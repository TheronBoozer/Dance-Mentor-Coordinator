import os
import requests

from Globals.Helpers import create_2d_array, get_flags, get_links, save_object, recycle_object, smtp_mailing
from Globals.file_paths import PICKLE_TEST, TEST_OUTLINE
from Objects.Google.Google_Form import Google_Form
from Objects.Google.Google_Sheet import Google_Sheet
from Objects.Location import Location
from Objects.Mentor import Mentor
from Objects.Session_Request import Session_Request


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

    # Initiation test
    statement = statement.replace("[FORM_ACCESS]", test_forms())

    # Confirmation test
    statement = statement.replace("[RESPONSE_GATHERING]", test_responses())

    # Update test
    statement = statement.replace("[SHEET_ACCESS]", test_sheets())

    # Emialing
    statement = statement.replace("[SUBJECT]", get_subject(statement))
    statement = statement.replace("[EMAILING]", green("Email succesful"))
    statement = statement.replace("Email succesful", test_email(statement))
        
    with open("Saved_Information/Test_Log.txt", 'w') as f:
        f.write(statement)
    # print(statement)


def get_os() -> str:
    operating_sys = os.name
    if operating_sys == 'nt':
        return yellow("Windows")
    elif operating_sys == 'posix':
        return green("Linux")
    else:
        return "Who the fuck knows"

def cron_check() -> str:
    operating_sys = os.name
    term = os.getenv("TERM")
    display = os.getenv("DISPLAY")

    if term == None and display == None and operating_sys == 'posix':
        return green("Run through Crontab")
    else:
        return yellow("Not run through Crontab")

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
    
def test_email(statement:str):
    try:
        recipient = get_flags()["SECRETARY_EMAIL"]
        subject = statement[statement.find("{")+1: statement.find("}")].replace("\n", "")
        smtp_mailing([recipient], subject, statement[statement.find("}")+2:])
        return green("Emailing successful")
    except Exception as e:
        return red("error emailing", repr(e))
    
    
# test scraping phase
def test_location() -> str:
    try:
        location_sheet = get_links()["LOCATION_INFORMATION_SHEET_LINK"]                 # fetch the location sheet link
        location_information = create_2d_array(location_sheet)                          # make a 2d array of the location information
        if(len(location_information)>0):
            Location(location_information[0])
        fin = f"{len(location_information)} locations found"
        return green(fin)
    except Exception as e:
        return red("Locations not found", repr(e))
    
def test_mentor() -> str:
    try:
        mentor_sheet = get_links()["DANCE_MENTOR_INFORMATION_SHEET_LINK"]                 # fetch the location sheet link
        mentor_information = create_2d_array(mentor_sheet)                          # make a 2d array of the location information
        if(len(mentor_information)>0):
            Mentor(mentor_information[0])
        fin = f"{len(mentor_information)} mentors found"
        return green(fin)
    except Exception as e:
        return red("Mentors not found", repr(e))
    
def test_session() -> str:
    try:
        session_sheet = get_links()["SESSION_REQUEST_SHEET_LINK"]                 # fetch the location sheet link
        session_information = create_2d_array(session_sheet, True)                          # make a 2d array of the location information
        if(len(session_information)>0):
            Session_Request(session_information[0])
        fin = f"{len(session_information)} sessions found"
        return green(fin)
    except Exception as e:
        return red("Sessions not found", repr(e))


# test initiation phase
def test_forms() -> str:
    try:
        form_link = get_links()["CONFIRMATION_FORM_EDIT_LINK"]
        Google_Form(form_link)
        return green("Form access granted")
    except Exception as e:
        return red("Form access denied", repr(e))
    

# test confirmaion phase
def test_responses() -> str:
    try:
        form_link = get_links()["CONFIRMATION_FORM_EDIT_LINK"]
        form = Google_Form(form_link)
        form.update_responses()
        return green("Response updating seccessful")
    except Exception as e:
        return red("Form responses innaccesible", repr(e))
    

# test update phase
def test_sheets() -> str:
    try:
        sheet_link = get_links()["SESSION_LOG_SHEET"]
        Google_Sheet(sheet_link)
        return green("Session log accessed")
    except Exception as e:
        return red("Session sheet inaccesible", repr(e))
    

def get_subject(statement:str) -> str:
    if "red" in statement:
        return "ERROR IN TESTING"
    else:
        return "All Systems Go"






def red(skk : str, error=None) -> str: 
    if error == None:
        return '<p style="color: red;">{}</p>' .format(skk)
    else:
        return '<p style="color: red;">{}, failed with error:<br>    {}</p>' .format(skk, error)
 
 
def green(skk : str) -> str: 
    return('<p style="color: green;">{}</p>' .format(skk))

def yellow(skk : str) -> str: 
    return('<p style="color: orange;">{}</p>' .format(skk))