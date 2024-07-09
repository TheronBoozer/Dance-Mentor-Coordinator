import datetime
import requests
import json
from Scheduled_Entities.Location import Location
from Scheduled_Entities.Mentor import Mentor
from Scheduled_Entities.Session_Request import Session_Request
import re



# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////*   PRIVATE METHODS   */////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////

def __get_links():
    """
    Fetches the links to the location and mentor google sheets
    """
    
    links = json.load(open('links.json'))           # open the file 'links.json'
    return links                                    # returns the dictionary


def __create_2d_array(link : str, recent : False):
    """
    Generates a 2d array from a given google sheet link
    """
    
    csv_link = link[:link.index('edit')] + 'export?format=tsv'      # converts basic 'share' link to a readable csv link

    google_sheet = requests.get(csv_link)                           # read the csv file made from the link
    unorganized_data = google_sheet.text                            # sorts it into only the text
    array_of_str_rows = unorganized_data.split('\r')                # splits the text into rows

    array_of_str_rows.pop(0)                                        # remove the label row

    if recent:
        array_of_str_rows = __remove_old_rows(array_of_str_rows)
            

    sheet_information = []                                          # create empty array to be filled with row arrays 

    for str_row in array_of_str_rows:                               # for each string
        row_array = str_row.split('\t')                              # split the row text by commas
        row_array.pop(0)                                            # delete the timestamp
        sheet_information.append(row_array)                         # add to the master array



    return sheet_information


def __remove_old_rows(rows):
    current_weekday = datetime.datetime.now(tz=None).weekday()
    days_since_last_saturday = ((current_weekday + (7-5)) % 7 + 6) 
    last_saturday_at_midnight = int(datetime.datetime.now(tz=None).timestamp()) - days_since_last_saturday * 24 * 3600 
    last_saturday_at_midnight -= last_saturday_at_midnight % (24*3600) - 4*3600 

    for row in rows[::-1]:
        fixed_format = row[:row.index("\t")].strip()     
        nums_in_format = re.findall(r"/d+", fixed_format)


        for num in nums_in_format:
            if len(num) == 1:
                fixed_format.replace(num, f"0{num}")

        timestamp = datetime.datetime.strptime(fixed_format, "%m/%d/%Y %H:%M:%S").timestamp()

        if int(timestamp) <  last_saturday_at_midnight:
            rows = rows[rows.index(row)+1:]
            break

    return rows


# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////*   PUBLIC METHODS   */////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////

def get_mentors():
    """
    Returns a dictionary of the dance mentors based on the google sheet link
    """
    
    mentor_sheet_link = __get_links()["DANCE_MENTOR_INFORMATION_SHEET_LINK"]        # fetch the mentor sheet link
    mentor_information = __create_2d_array(mentor_sheet_link)                       # make a 2d array of the mentor information

    mentors = {}                                                                    # create final dictionary
    for information in mentor_information:                                          # for each array in the 2d array
        mentors[information[0]] = Mentor(information)                               # add an entry to the dictionary -> 'name' : Mentor

    return mentors
                
def get_locations():
    """
    Returns a dictionary of the practice locations based on the google sheet link
    """
    
    location_sheet = __get_links()["LOCATION_INFORMATION_SHEET_LINK"]               # fetch the location sheet link
    location_information = __create_2d_array(location_sheet)                        # make a 2d array of the location information

    locations = {}                                                                  # create final dictionary
    for information in location_information:                                        # for each array in the 2d array
        locations[information[0]] = Location(information)                           # add an entry to the dictionary -> 'name' : Location

    return locations

def get_sessions():
    """
    Returns an array of the recent session requests
    """

    session_sheet = __get_links()["SESSION_REQUEST_SHEET_LINK"]
    session_information = __create_2d_array(session_sheet, True)

    sessions = []
    for information in session_information:
        sessions.append(Session_Request(information))

    return sessions
