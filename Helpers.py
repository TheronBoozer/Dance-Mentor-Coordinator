import datetime
import requests
import json
from Scheduled_Entities.Google_Form import Google_Form
from Scheduled_Entities.Location import Location
from Scheduled_Entities.Mentor import Mentor
from Scheduled_Entities.Session_Request import Session_Request
import win32com.client as win32




# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////*   PRIVATE METHODS   */////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////

def __get_links():
    """
    Fetches the links to the location and mentor google sheets
    """
    
    links = json.load(open('Saved_Information/links.json'))           # open the file 'links.json'
    return links                                    # returns the dictionary


def __create_2d_array(link : str, recent = False):
    """
    Generates a 2d array from a given google sheet link
    """
    
    csv_link = link[:link.index('edit')] + 'export?format=tsv'      # converts basic 'share' link to a readable csv link

    google_sheet = requests.get(csv_link)                           # read the csv file made from the link
    unorganized_data = google_sheet.text                            # sorts it into only the text
    array_of_str_rows = unorganized_data.split('\r')                # splits the text into rows

    array_of_str_rows.pop(0)                                        # remove the label row


    if recent:                                                      # if only the recent rows are requested
        array_of_str_rows = __remove_old_rows(array_of_str_rows)    # remove the old ones
            

    sheet_information = []                                          # create empty array to be filled with row arrays 

    for str_row in array_of_str_rows:                               # for each string
        row_array = str_row.split('\t')                              # split the row text by commas
        row_array.pop(0)                                            # delete the timestamp
        sheet_information.append(row_array)                         # add to the master array



    return sheet_information


def __remove_old_rows(rows):
    """
    A function that removes rows with a timestamp older than the last 'initial' phase
    """
    
    last_week_timing = weekly_timing("initiation")                                                      # get the unix timestamp of last weeks run

    for row in rows[::-1]:                                                                              # loop throw each row from the back
        fixed_format = row[:row.index("\t")].strip()                                                    # grab just the timestamp
        timestamp = datetime.datetime.strptime(fixed_format, "%m/%d/%Y %H:%M:%S").timestamp()           # create the integer timestamp from the readable one

        if int(timestamp) <  last_week_timing:                                                          # if the timestamp is older than last saturday
            rows = rows[rows.index(row)+1:]                                                             # clip the row array to only hold those more recent ones
            break

    return rows


def __get_form() -> Google_Form:
    """
    Returns a Google_Form object for the Mentor request selection form
    """

    form_link = __get_links()["CONFIRMATION_FORM_EDIT_LINK"]                        # fetch the form link
    return Google_Form(form_link)                                                   # get the form with that link



# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////*   PUBLIC METHODS   */////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////

def get_mentors():
    """
    Returns a list of the dance mentors based on the google sheet link
    """
    
    mentor_sheet_link = __get_links()["DANCE_MENTOR_INFORMATION_SHEET_LINK"]        # fetch the mentor sheet link
    mentor_information = __create_2d_array(mentor_sheet_link)                       # make a 2d array of the mentor information

    mentors = []                                                                    # create final array
    for information in mentor_information:                                          # for each array in the 2d array
        mentors.append(Mentor(information))                                         # add an entry to the dictionary -> 'name' : Mentor

    return mentors
                
def get_locations():
    """
    Returns a list of the practice locations based on the google sheet link
    """
    
    location_sheet = __get_links()["LOCATION_INFORMATION_SHEET_LINK"]               # fetch the location sheet link
    location_information = __create_2d_array(location_sheet)                        # make a 2d array of the location information

    locations = []                                                                  # create final array
    for information in location_information:                                        # for each array in the 2d array
        locations.append(Location(information))                                     # add to the array

    return locations

def get_sessions():
    """
    Returns an array of the recent session requests
    """

    session_sheet = __get_links()["SESSION_REQUEST_SHEET_LINK"]                     # fetch the session sheet link
    session_information = __create_2d_array(session_sheet, True)                    # make a 2d array of the recent session info 

    sessions = []                                                                   # create final array
    for information in session_information:                                         # for each array in the 2d array
        sessions.append(Session_Request(information))                               # add to the array

    return sessions
    

def make_initial_form(mentors : list, locations : list, sessions : list):
    """
    set up the initial DM time selection google form
    """
    
    form = __get_form()                                                                 # get the confirmation form link
    form.clear_form()                                                                   # remove all current questions and sections

    expressions = json.load(open('Saved_Information/expressions.json'))["FORM"]         # grab the expressions used in the form
    mentor_names = []                                                                   # create the initial array of mentors

    for i, mentor in enumerate(mentors):                                                                                    # for each mentor
        no_sessions = True                                                                                                  # create a boolean tracking session amounts
        mentor_names.append(mentor.get_name())                                                                              # add the name to the list
        form.add_recipient(mentor.get_email())                                                                              # add their email to the email list
        form.add_section(mentor.get_name(), expressions["MENTOR_SECTION_HEADER"], id=f'{i+1}0000')                          # add their section header with proper id

        for j, session in enumerate(sessions):                                                                              # for each session 
            session_id = '0' * (4-len(str(i + 1))) + str(i + 1) + '0' * (4-len(str(j + 1))) + str(j+1)                      # create the question id
            if form.make_session_request_question(mentor, locations, session, question_id=session_id) is not None:          # if at any point it creates a question
                no_sessions = False                                                                                         # change no_sessions to false

        if no_sessions:                                                                                                     # if they have no sessions
            form.add_text(expressions["NO_SESSIONS_TITLE"], expressions["NO_SESSIONS_DESCRIPTION"])                         # add the no sessions text


    form.add_multiple_choice_question(                                                  # add the starting mentor selection question 
        expressions["NAME_SELECTION"], 
        None, 
        mentor_names, 
        section_selection=True, 
        index=0, 
        id='00000000'
        )

    return form


def send_form(form : Google_Form):
    """
    sends an email with an attached google form
    """
    
    outlook = win32.Dispatch('outlook.application')                                             # find the outlook application
    form_link = f'https://docs.google.com/forms/d/{form.get_id()}/viewform'                     # get the form share link

    expressions = json.load(open('Saved_Information/expressions.json'))["INITIAL_EMAIL"]        # grab the expressions used in the email

    mail = outlook.CreateItem(0)                                                                # create an email item
    mail.To = form.get_recipients()                                                             # send the email to the form recipients
    mail.Subject = expressions["SUBJECT"]                                                       # set the subject
    mail.Body = expressions["BODY"].replace("CONFIRMATION_FORM_LINK", form_link)                # set the body including the confirmation link
    
    mail.Send()


def weekly_timing(phase : str, last_week=True):
    """
    convert an array in the form ["weekday", hour, minute] into the unix timestamp of the past week
        set last_week to False to grab the most recent one
    """

    phase_time = json.loads(open('Saved_Information/timing'))[phase]                                            # grab what time the program is meant to run each week

    weekday_reference = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]          # create a weekday reference array

    current_weekday = datetime.datetime.now().weekday()                                                         # get what weekday it is today
    target_weekday = weekday_reference.index(phase_time[0].capitalize())                                        # convert the weekday string to the numeric interpretation

    current_time = int(datetime.datetime.now().timestamp())                                                     # get the current timestamp
    target_hour = phase_time[1]                                                                                 # save the target hour in military time
    target_minute = phase_time[2]                                                                               # save the target minute

    days_between_target_and_now = (current_weekday + (7 - target_weekday)) % 7 + 7 * int(last_week)             # some math to find how many days have passed since the target day

    target_day = current_time - days_between_target_and_now * 24 * 3600                                         # get to the correct unix day
    target_time = target_day - target_day % (24*3600) - 4*3600 + target_hour*3600 + target_minute*60            # remove any residual time then add to get back to the target including fixing for timezones

    return target_time