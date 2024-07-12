from apiclient import discovery
from oauth2client import file, tools

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


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
        for answer in answers:
            option = {"value": answer}
            if section_selection:
                section_id = answer.replace(' ', '_')
                option['goToSectionId'] = section_id
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
    

    def add_section(self, title : str, description):

        questions = self.form_service.forms().get(formId=self.form_id).execute()
        num_of_questions = len(questions.get('items', []))

        item_id = title.replace(' ', '_')
    
        NEW_SECTION = {
            "requests": [
                {
                    "createItem": {
                        "item": {
                            "itemId" : (
                                item_id
                            ),
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

        return (
            self.form_service.forms()
            .batchUpdate(formId=self.form_id, body=NEW_SECTION)
            .execute()
        )