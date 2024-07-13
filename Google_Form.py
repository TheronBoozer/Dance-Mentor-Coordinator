from apiclient import discovery
from oauth2client import file, tools

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from Scheduled_Entities.Mentor import Mentor
from Scheduled_Entities.Session_Request import Session_Request


SCOPES = ['https://www.googleapis.com/auth/forms.body']
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

        start_index = link.find('/e/')
        if start_index == -1:
            start_index = link.find('/d/')

        self.form_id = link[start_index+3:link.rindex('/')]
        self.form_service = self.__setup_form_service()
        self.sections = {}



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
        
        store = file.Storage("token.json")
        creds = None
        if os.path.exists("token.json") :
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid :
            if creds and creds.expired and creds.refresh_token :
                creds.refresh(Request())
            else :
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_oauth.json', SCOPES
                )
                creds = tools.run_flow(flow, store)
            with open('token.json', 'w') as token :
                token.write(creds.to_json())

        form_service = discovery.build(
            "forms",
            "v1",
            credentials=creds,
            discoveryServiceUrl=DISCOVERY_DOC,
            static_discovery=False,
        )
        return form_service
    


    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////*   PUBLIC METHODS   */////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def clear_form(self):
        """
        Clears all questions and descriptions from the form
        """
        
        questions = self.form_service.forms().get(formId=self.form_id).execute()
        questions = questions.get('items', [])

        if len(questions) == 0: return

        delete_requests = []

        for i, item in enumerate(questions):
            if 'title' in item:
                delete_requests.append({"deleteItem": {"location": {"index": i}}})
        delete_requests.reverse()

        batch_delete_request = {"requests" : delete_requests}

        self.form_service.forms().batchUpdate(formId=self.form_id, body=batch_delete_request).execute()

    
    def add_multiple_choice_question(self, title, description, answers, type='RADIO', required=True, section_selection=False, index=-1):
        """
        Adds a multiple choice question to the given form with specified title, description, and answers
          The parameters -
            'type' changes between RADIO, CHECKBOX, and DROP_DOWN which changes the type of answer that can be provided
            'section_selection' lets you decide if a question should redirect a user to a new section based on their answer - the answer must have the same name as the section title
        """
        
        options = []
        for i, answer in enumerate (answers):
            option = {"value": answer}
            if section_selection:
                option['goToSectionId'] = str(i)
            options.append(option)

        if index == -1:
            questions = self.form_service.forms().get(formId=self.form_id).execute()
            index = len(questions.get('items', []))

        NEW_QUESTION = {
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


        return (
            self.form_service.forms()
            .batchUpdate(formId=self.form_id, body=NEW_QUESTION)
            .execute()
        )
    

    def add_section(self, title : str, description, id=None):

        questions = self.form_service.forms().get(formId=self.form_id).execute()
        num_of_questions = len(questions.get('items', []))
    
        NEW_SECTION = {
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

        if id is not None:
            NEW_SECTION["requests"][0]["createItem"]["item"]["itemId"] = id

        return (
            self.form_service.forms()
            .batchUpdate(formId=self.form_id, body=NEW_SECTION)
            .execute()
        )
    
    def add_text(self, title : str, description):

        questions = self.form_service.forms().get(formId=self.form_id).execute()
        num_of_questions = len(questions.get('items', []))
    
        NEW_SECTION = {
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

        return (
            self.form_service.forms()
            .batchUpdate(formId=self.form_id, body=NEW_SECTION)
            .execute()
        )

    def make_session_request_question(self, mentor : Mentor, locations : list, request : Session_Request):
        possible_times = mentor.get_schedule().cross_check_with(request.get_schedule())
        if len(possible_times) == 0:
            self.add_text("You have no sessions", "This either means there are no sessions this week, or that your availability doesn't line up.\nTry again next week!")
            return
        title = request.get_partiicipants()
        description = f"{title} \n\n {request.get_description()}"

        options = ["I do not want this session"]
        times = []

        for location in locations:
            location_timing = location.get_schedule().cross_check_with(possible_times)
            for time in location_timing:
                if time not in times:
                    times.append(time)
                    options.append(f"{str(time)} - {location.get_name()}")


        self.add_multiple_choice_question(title, description, options, type="DROP_DOWN")