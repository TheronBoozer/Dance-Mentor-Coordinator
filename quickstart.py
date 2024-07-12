from apiclient import discovery
from oauth2client import client, file, tools
from Helpers import save_object, recycle_object

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ['https://www.googleapis.com/auth/forms.body']
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

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

# Request body for creating a form
# NEW_FORM = {
#     "info": {
#         "title": "Quickstart form",
#     }
# }

# Request body to add a multiple-choice question
NEW_QUESTION = {
    "requests": [
        {
            "createItem": {
                "item": {
                    "title": (
                        "In what year did the United States land a mission on"
                        " the moon?"
                    ),
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [
                                    {"value": "1965"},
                                    {"value": "1967"},
                                    {"value": "1969"},
                                    {"value": "1971"},
                                ],
                                "shuffle": True,
                            },
                        }
                    },
                },
                "location": {"index": 0},
            }
        }
    ]
}

# Creates the initial form
# result = form_service.forms().create(body=NEW_FORM).execute()

# Adds the question to the form
question_setting = (
    form_service.forms()
    .batchUpdate(formId="1S0D8c-8_oXHXEF687RoDfXnxxnqM9ZLXJHNiLlparqo", body=NEW_QUESTION)
    .execute()
)



# Prints the result to show the question has been added
get_result = form_service.forms().get(formId="1S0D8c-8_oXHXEF687RoDfXnxxnqM9ZLXJHNiLlparqo").execute()
print(get_result)


def clear_form(form_id):
    questions = form_service.forms().get(formId=form_id).execute()
    questions = questions.get('items', [])

    print (questions)

    delete_requests = []

    for i, item in enumerate(questions):
        if 'title' in item and 'questionItem' in item:
            delete_requests.append({"deleteItem": {"location": {"index": i}}})
    delete_requests.reverse()

    batch_delete_request = {"requests" : delete_requests}

    form_service.forms().batchUpdate(formId=form_id, body=batch_delete_request).execute()
    
clear_form("1S0D8c-8_oXHXEF687RoDfXnxxnqM9ZLXJHNiLlparqo")