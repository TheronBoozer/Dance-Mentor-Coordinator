import json
from apiclient import discovery
from oauth2client import client, file, tools

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


from Scheduled_Entities.Mentor import Mentor
from Scheduled_Entities.Session_Request import Session_Request


SCOPES = ['https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/forms.responses.readonly']
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

class Google_Form:
    """
    Creates an editable google form object
    """
    


    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////*   INITIALIZER   *///////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, link : str):

        start_index = link.find('/d/') + 3                              # find the start of the form ID

        self.form_id = link[start_index:link.rindex('/')]               # clip the id out of the url
        self.form_service = self.__setup_form_service()                 # set up the form recognition and such
        self.recipients = []                                            # create an empty list of emails for the form to be sent to

        self.responses = []                                             # cretae the list of responses to be filled later



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////*   PRIVATE METHODS   */////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __setup_form_service(self):
        """
        Sets up the authentication for the form in question
        If not previously authenticated, the setup will need to be manually verified
        """
        
        creds = None                                                                        # create credentials

        if os.path.exists("Saved_Information/token.json") :                                                   # if the file 'token.json' exists
            creds = Credentials.from_authorized_user_file('Saved_Information/token.json', SCOPES)             # make credentials from the saved token

        if not creds or not creds.valid or not creds.scopes == SCOPES:                      # if the credentials weren't set or are invalid and the necessary scopes are provided

            if creds and creds.expired and creds.refresh_token :                            # if the credentials expired
                creds.refresh(Request())                                                    # refresh them from the token
            else :                                                                          # otherwise
                store = file.Storage("Saved_Information/token.json")                        # grab or make the saved credentials token
                flow = client.flow_from_clientsecrets(                                      # authenticate manually
                    'Saved_Information/client_oauth.json', SCOPES
                )
                creds = tools.run_flow(flow, store)                                         # update the credentials from the manual authentication

            with open('Saved_Information/token.json', 'w') as token :                       # open 'tokens.json'
                token.write(creds.to_json())                                                # save the credentials to the json file


        form_service = discovery.build(                                                     # create the google api service for all future use
            "forms",
            "v1",
            credentials=creds,
            discoveryServiceUrl=DISCOVERY_DOC,
            static_discovery=False,
        )

        return form_service
    

    def update_responses(self):
        self.responses = self.form_service.forms().responses().list(formId=self.form_id).execute()
        print(self.responses)
    


    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////*   PUBLIC METHODS   */////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def clear_form(self):
        """
        Clears all questions and descriptions from the form
        """
        
        form = self.form_service.forms().get(formId=self.form_id).execute()                     # get the form used
        questions = form.get('items', [])                                                       # find all the items inthe form

        if len(questions) == 0: return form                                                     # if the form is already emtpy, return the form

        delete_requests = []                                                                    # create the array of requests

        for i, item in enumerate(questions):                                                    # for each item in the form
            if 'title' in item:                                                                 # if the item has a title
                delete_requests.append({"deleteItem": {"location": {"index": i}}})              # add the index of the item to the delete requests

        delete_requests.reverse()                                                               # reverse the list to avoid index errors

        batch_delete_request = {"requests" : delete_requests}                                   # create the batch request item

        return (                                                                                # return the form
            self.form_service
            .forms()
            .batchUpdate(formId=self.form_id, body=batch_delete_request)                        # delete all the requested items
            .execute()
        )

    
    def add_multiple_choice_question(self, title, description, answers, type='RADIO', required=True, section_selection=False, index=-1, id=None, last_page=False):
        """
        Adds a multiple choice question to the given form with specified title, description, and answers
          The parameters -
            'type' changes between RADIO, CHECKBOX, and DROP_DOWN which changes the type of answer that can be provided
            'section_selection' lets you decide if a question should redirect a user to a new section based on their answer - the answer must have the same name as the section title
        """
        
        options = []                                                                            # create the options array
        for i, answer in enumerate (answers):                                                   # for every provided answer
            option = {"value": answer}                                                          # create the option dictionary
            if section_selection:                                                               # if the function was called with section selection on
                option['goToSectionId'] = f'{i+1}0000'                                          # add the command to go to a section based on the order of the questions
            if last_page:
                option['goToAction'] = 'SUBMIT_FORM'
            options.append(option)                                                              # add that option to the big list for later

        if index == -1:                                                                         # if no index was provided
            form = self.form_service.forms().get(formId=self.form_id).execute()                 # get the form
            index = len(form.get('items', []))                                                  # make the index the end of the questions

        NEW_QUESTION = {                                                                        # make the question item
            "requests": [
                {
                    "createItem": {
                        "item": {
                            "title": (
                                title
                            ),
                            "description" : (
                                description
                            ),
                            "questionItem": {
                                "question": {
                                    "required": required,
                                    "choiceQuestion": {
                                        "type": type,
                                        "options": options,
                                    },
                                }
                            },
                        },
                        "location": {"index": index},
                    }
                }
            ]
        }

        if id is not None:                                                                      # if there was a given id
            NEW_QUESTION["requests"][0]["createItem"]["item"]["questionItem"]["question"]["questionId"] = id                     # add a custom itemId to the item

        return (                                                                                # return the form
            self.form_service.forms()
            .batchUpdate(formId=self.form_id, body=NEW_QUESTION)                                # create the questions
            .execute()
        )
    

    def add_section(self, title : str, description, id=None):
        """
        Adds a section page to the google form
        """

        form = self.form_service.forms().get(formId=self.form_id).execute()                     # get the form
        num_of_questions = len(form.get('items', []))                                           # get the number of items in the form
    
        NEW_SECTION = {                                                                         # create the section item
            "requests": [
                {
                    "createItem": {
                        "item": {
                            "title": (
                                title
                            ),
                            "description" : (
                                description
                            ),
                            "pageBreakItem": {
                            },
                        },
                        "location": {"index": num_of_questions},
                    }
                }
            ]
        }

        if id is not None:                                                                      # if there was a given id
            NEW_SECTION["requests"][0]["createItem"]["item"]["itemId"] = id                     # add a custom itemId to the item

        return (                                                                                # return the form
            self.form_service.forms()
            .batchUpdate(formId=self.form_id, body=NEW_SECTION)                                 # add the new section
            .execute()
        )
    
    def add_text(self, title : str, description):
        """
        Adds a text item to the google form
        """
        
        form = self.form_service.forms().get(formId=self.form_id).execute()                     # get the form
        num_of_questions = len(form.get('items', []))                                           # get the number of items in the form
    
        NEW_SECTION = {                                                                         # create the text item
            "requests": [
                {
                    "createItem": {
                        "item": {
                            "title": (
                                title
                            ),
                            "description" : (
                                description
                            ),
                            "textItem": {
                            },
                        },
                        "location": {"index": num_of_questions},
                    }
                }
            ]
        }

        return (                                                                                # return the form
            self.form_service.forms()
            .batchUpdate(formId=self.form_id, body=NEW_SECTION)                                 # add the new text
            .execute()
        )


    def make_session_request_question(self, mentor : Mentor, locations : list, request : Session_Request, question_id=None):
        """
        Creates a form question based on mentor and location availability
        """

        file = json.load(open('Saved_Information/expressions.json'))
        expressions = file["FORM"]

        possible_times = mentor.get_schedule().cross_check_with(request.get_schedule())         # cross check the mentors schedule with the session schedule

        if len(possible_times) == 0:                                                            # if there are no possible times 
            return None                                                                         # return nothing
        
        title = f'{request.get_partiicipants()} session request'                                # create the title based on the participating party
        description = f"{request.get_topic()} \n\n {request.get_description()}"                 # create the body of the question with the topic and added description

        options = [expressions["SESSION_REJECTION"]]                                            # create the answer options with the default rejecting answer
        times = []                                                                              # create the list of times

        for location in locations:                                                              # for each given practice location
            location_timing = location.get_schedule().cross_check_with(possible_times)          # find the overlapping available times
            for time in location_timing:                                                        # for those times
                if time not in times:                                                           # if the time is not already listed
                    times.append(time)                                                          # add it to the list
                    options.append(f"{str(time)} - {location.get_name()}")                      # add the option for that time


        self.add_multiple_choice_question(title, description, options, type="DROP_DOWN", id=question_id, last_page=True)        # add a drop down question with the time options as answers


    def add_recipient(self, email : str):
        """
        Add an email to the listing this form will be sent to
        """
        
        self.recipients.append(email)                                                           # add the email to the saved list



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////*   GETTERS   *////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def get_recipients(self):
        return self.recipients
    
    def get_id(self):
        return self.form_id