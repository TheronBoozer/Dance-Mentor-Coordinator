import json
import win32com.client as win32

from Function_Phases.Helpers import get_links
from Scheduled_Entities.Google_Form import Google_Form



def send_out_initial_form(info) -> Google_Form:
    """
    assigns the proper data and then makes and emails the initial form
    """
    
    mentor_list = info["mentor_list"]                                                           # set the mentor list
    location_list = info["location_list"]                                                       # set the location list
    session_requests = info["session_requests"]                                                 # set the session list

    form = make_initial_form(mentor_list, location_list, session_requests)                      # create the form

    # send_form(form) TODO: test this                                                           # email the form out
    
    return form


def get_initial_form() -> Google_Form:
    """
    Returns a Google_Form object for the Mentor request selection form
    """

    form_link = get_links()["CONFIRMATION_FORM_EDIT_LINK"]                                      # fetch the form link
    return Google_Form(form_link)                                                               # get the form with that link


def make_initial_form(mentors : list, locations : list, sessions : list):
    """
    set up the initial DM time selection google form
    """
    
    form = get_initial_form()                                                                                               # get the confirmation form link
    form.clear_form()                                                                                                       # remove all current questions and sections

    expressions = json.load(open('Saved_Information/expressions.json'))["FORM"]                                             # grab the expressions used in the form
    mentor_names = []                                                                                                       # create the initial array of mentors

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


    form.add_multiple_choice_question(                                                                                      # add the starting mentor selection question 
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

