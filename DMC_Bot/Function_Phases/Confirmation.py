# external imports
import json

# internal references
from DMC_Bot import flags
from Scheduled_Entities.Session_Request import Session_Request
from Function_Phases.Helpers import smtp_mailing, weekday_to_date, recycle_object, save_object


def create_session_pairings():

    form = recycle_object('Saved_Information/confirmation_form.pkl')
    info = recycle_object('Saved_Information/scheduled_entities.pkl')


    mentor_list = info["mentor_list"]
    session_requests = info["session_requests"]

    if not session_requests:
        return

    responses = form.update_responses()

    rejected_expression = json.load(open('Saved_Information/expressions.json'))["FORM"]["SESSION_REJECTION"]

    for response in responses:
        for question in response["answers"].values():
            
            question_id = question["questionId"]

            if question_id == "00000000" or 'b' in question_id:
                continue

            session_id = question_id[5:]
            mentor_id = question_id[:4]
            linked_question = response["answers"][question_id.replace('a', 'b')]

            answer = question["textAnswers"]["answers"][0]["value"]
            
            match_rating = int(linked_question["textAnswers"]["answers"][0]["value"]) * 10
            if not answer == rejected_expression:
                session_requests[int(session_id) - 1].add_mentor_option([match_rating, mentor_list[int(mentor_id) - 1], answer])


    if flags.EMAIL_ON:
        send_final_emails(session_requests)

    # form.deleteAllResponses()


def send_final_emails(sessions):
    mega_session_list = []

    for session in sessions:
        mega_session_list.append(send_email(session))

    save_object(mega_session_list, 'Saved_Information/Session_Log.pkl')


def send_email(session : Session_Request):
    """
    sends an email with the session details
    """
    
    # outlook = win32.Dispatch('outlook.application')                                             # find the outlook application

    email_outline = open('Saved_Information/Secondary_Email_Confirmation.txt', 'r')       # grab the expressions used in the email
    email_outline = email_outline.read()
    subject = email_outline[email_outline.index('{')+1 : email_outline.index('}')]
    body = email_outline.replace(subject, "")[3:]

    mentee_names = session.get_participants()
    mentor = session.get_mentor()[1]

    mentee_emails = session.get_emails()

    if mentor == None:
        # sedn rejection email
        return send_rejection(session)

    mentor_name = mentor.get_name()
    mentor_email = mentor.get_email()

    mentor_phone_number = mentor.get_phone_number()
    mentee_phone_numbers = session.get_numbers()

    when_and_where = session.get_mentor()[2]
    weekday = when_and_where[:when_and_where.index(" ")]
    day = weekday_to_date(weekday)
    time = when_and_where[when_and_where.index(" from "):when_and_where.index(" at ")]

    location = when_and_where[when_and_where.index("at ")+3:]
    datetime = f'{weekday}, {day}{time}'

    topic = session.get_topic()
    description = session.get_description()

    body = body.replace("[MENTEE_NAMES]", mentee_names)
    body = body.replace("[TIME]", datetime)
    body = body.replace("[MENTOR_NAME]", mentor_name)
    body = body.replace("[LOCATION]", location)
    body = body.replace("[MENTOR_PHONE_NUMBER]", mentor_phone_number)
    body = body.replace("[MENTOR_EMAIL]", mentor_email)
    body = body.replace("[MENTEE_PHONE_NUMBERS]", ", ".join(mentee_phone_numbers))
    body = body.replace("[MENTEE_EMAILS]", ", ".join(mentee_emails))
    body = body.replace("[SESSION_TOPIC]", topic)
    body = body.replace("[SESSION_DESCRIPTION]", description)

    mentee_emails.append(mentor_email)
    recipients = mentee_emails
    # mail = outlook.CreateItem(0)                                                                # create an email item
    # mail.To = ";".join(recipients)                                                              # send the email to the form recipients
    # mail.Subject = subject                                                                      # set the subject
    # mail.Body = body                                                                            # set the body including the confirmation link
    
    # mail.Send()
    smtp_mailing(recipients, subject, body)


    return [mentor_name, mentee_names, datetime]


def send_rejection(session : Session_Request):
    emails = session.get_emails()
    names = session.get_participants()
    topic = session.get_topic()
    description = session.get_description()

    # outlook = win32.Dispatch('outlook.application')                                             # find the outlook application

    email_outline = open('Saved_Information/Secondary_Email_Confirmation.txt', 'r')       # grab the expressions used in the email
    email_outline = email_outline.read()
    subject = email_outline[email_outline.index('{')+1 : email_outline.index('}')]
    body = email_outline.replace(subject, "")[3:]

    body = body.replace("[MENTEE_NAMES]", names)
    body = body.replace("[SESSION_TOPIC]", topic)
    body = body.replace("[SESSION_DECRIPTION]", description)

    recipients = emails
    # mail = outlook.CreateItem(0)                                                                # create an email item
    # mail.To = ";".join(recipients)                                                             # send the email to the form recipients
    # mail.Subject = subject                                                       # set the subject
    # mail.Body = body                # set the body including the confirmation link
    
    # mail.Send()
    smtp_mailing(recipients, subject, body)