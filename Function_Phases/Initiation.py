import json
import win32com.client as win32

from Function_Phases.Helpers import get_links, recycle_object, save_object, smtp_mailing
from Scheduled_Entities.Google_Form import Google_Form




def send_out_initial_form(email_on = True) -> Google_Form:
    """
    assigns the proper data and then makes and emails the initial form
    """
    info = recycle_object('Saved_Information/scheduled_entities.pkl')
    
    mentor_list = info["mentor_list"]                                                           # set the mentor list
    location_list = info["location_list"]                                                       # set the location list
    session_requests = info["session_requests"]                                                 # set the session list

    form = make_initial_form(mentor_list, location_list, session_requests)                      # create the form

    if email_on:
        send_form(form)                                                                         # email the form out

    save_object(form, 'Saved_Information/confirmation_form.pkl')
    
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
        title = expressions["MENTOR_SECTION_TITLE"].replace("[NAME]", mentor.get_name())                                    # create the title using the mentor name
        form.add_section(title, expressions["MENTOR_SECTION_HEADER"], id=f'{i+1}0000')                                      # add their section header with proper id

        for j, session in enumerate(sessions):                                                                              # for each session 
            session_id = '0' * (4-len(str(i + 1))) + str(i + 1) + 'a' + '0' * (3-len(str(j + 1))) + str(j+1)                # create the question id
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
    
    # outlook = win32.Dispatch('outlook.application')                                             # find the outlook application
    form_link = f'https://docs.google.com/forms/d/{form.get_id()}/viewform'                     # get the form share link

    body = open('Saved_Information/Initial_Mentor_Email.txt', 'r')                              # grab the email file
    body = body.read()                                                                          # read it
    subject = body[body.index('{')+1:body.index('}')]                                           # parse the subject
    body = body.replace(subject, "")[3:]                                                        # remove subject

    recipients = form.get_recipients()

    body = body.replace("[CONFIRMATION_FORM_LINK]", form_link)                                  # replace the confirmation

    # mail = outlook.CreateItem(0)                                                                # create an email item
    # mail.To = ";".join(form.get_recipients())                                                   # send the email to the form recipients
    # mail.Subject = subject                                                                      # set the subject
    # mail.Body = body                                                                            # set the body
    
    # mail.Send()
    smtp_mailing(recipients, subject, body)

