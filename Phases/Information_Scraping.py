# internal references
from Globals.Helpers import get_links, create_2d_array, save_object
from Objects.Location import Location
from Objects.Mentor import Mentor
from Objects.Session_Request import Session_Request

from Globals.file_paths import SAVED_OBJECTS

def get_weekly_information():
    """
    creates the mentor/location/session information dictionary
    """
    # global information
    information = {                                                                 # create the final dictionary of information
        "mentor_list" : get_mentors(),                                              # set the mentor information
        "location_list" : get_locations(),                                          # set the location information
        "session_requests" : get_sessions(),                                        # set the session information
    }

    save_object(information, SAVED_OBJECTS)
    
    return information


def get_mentors():
    """
    Returns a list of the dance mentors based on the google sheet link
    """
    
    mentor_sheet_link = get_links()["DANCE_MENTOR_INFORMATION_SHEET_LINK"]          # fetch the mentor sheet link
    mentor_information = create_2d_array(mentor_sheet_link)                         # make a 2d array of the mentor information

    mentors = []                                                                    # create final array
    for information in mentor_information:                                          # for each array in the 2d array
        mentors.append(Mentor(information))                                         # add an entry to the dictionary -> 'name' : Mentor

    return mentors


def get_locations():
    """
    Returns a list of the practice locations based on the google sheet link
    """
    
    location_sheet = get_links()["LOCATION_INFORMATION_SHEET_LINK"]                 # fetch the location sheet link
    location_information = create_2d_array(location_sheet)                          # make a 2d array of the location information

    locations = []                                                                  # create final array
    for information in location_information:                                        # for each array in the 2d array
        locations.append(Location(information))                                     # add to the array

    return locations


def get_sessions():
    """
    Returns an array of the recent session requests
    """

    session_sheet = get_links()["SESSION_REQUEST_SHEET_LINK"]                       # fetch the session sheet link
    session_information = create_2d_array(session_sheet, True)                      # make a 2d array of the recent session info 

    sessions = []                                                                   # create final array
    for information in session_information:                                         # for each array in the 2d array
        sessions.append(Session_Request(information))                               # add to the array

    
    return sessions
 