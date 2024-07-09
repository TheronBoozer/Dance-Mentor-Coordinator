import requests
import json
from Scheduled_Entities.Location import Location
from Scheduled_Entities.Mentor import Mentor



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


def __create_2d_array(link):
    """
    Generates a 2d array from a given google sheet link
    """
    
    csv_link = link[:link.index('edit')] + 'export?format=csv'      # converts basic 'share' link to a readable csv link

    google_sheet = requests.get(csv_link)                           # read the csv file made from the link
    unorganized_data = google_sheet.text                            # sorts it into only the text
    array_of_str_rows = unorganized_data.split('\r')                # splits the text into rows

    sheet_information = []                                          # create empty array to be filled with row arrays 

    for str_row in array_of_str_rows:                               # for each string
        row_array = str_row.split(',')                              # split the row text by commas
        row_array.pop(0)                                            # delete the timestamp
        sheet_information.append(row_array)                         # add to the master array

    sheet_information.pop(0)                                        # remove the label row

    return sheet_information



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

