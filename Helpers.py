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
    """
    A function that removes rows with a timestamp older than the past saturday
    """
    
    current_weekday = datetime.datetime.now().weekday()                                                                         # get the current weekday from 0-6 Monday-Sunday
    days_since_last_saturday = ((current_weekday + (7-5)) % 7 + 6)                                                              # some math to shift the current weekday to be the days since two saturdays ago
    last_saturday_at_midnight = int(datetime.datetime.now().timestamp()) - days_since_last_saturday * 24 * 3600                 # subtract the days from the current datetime
    last_saturday_at_midnight -= last_saturday_at_midnight % (24*3600) - 4*3600                                                 # remove residual hours and minutes so it's midnight on saturday

    for row in rows[::-1]:                                                                              # loop throw each row from the back
        fixed_format = row[:row.index("\t")].strip()                                                    # grab just the timestamp
        timestamp = datetime.datetime.strptime(fixed_format, "%m/%d/%Y %H:%M:%S").timestamp()           # create the integer timestamp from the readable one

        if int(timestamp) <  last_saturday_at_midnight:                                                 # if the timestamp is older than last saturday
            rows = rows[rows.index(row)+1:]                                                             # clip the row array to only hold those more recent ones
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
