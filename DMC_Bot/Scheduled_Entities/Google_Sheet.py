from apiclient import discovery
from oauth2client import client, file, tools

import os.path

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials




SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/forms']
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

class Google_Sheet:
    """
    Creates an editable google sheet object
    """
    


    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////*   INITIALIZER   *///////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, link : str):

        start_index = link.find('/d/') + 3                              # find the start of the sheet ID

        self.sheet_id = link[start_index:link.rindex('/')]               # clip the id out of the url
        self.sheet_service = self.__setup_sheet_service()                 # set up the sheet recognition and such




    def __setup_sheet_service(self):
        """
        Sets up the authentication for the sheet in question
        If not previously authenticated, the setup will need to be manually verified
        """
        
        creds = None                                                                        # create credentials
        reload_needed = False

        if os.path.exists("Saved_Information/token.json") :                                                   # if the file 'token.json' exists
            creds = Credentials.from_authorized_user_file('Saved_Information/token.json')             # make credentials from the saved token

        if not creds or not creds.valid or not creds.scopes == SCOPES:                      # if the credentials weren't set or are invalid and the necessary scopes are provided

            if creds and creds.expired and creds.refresh_token :                            # if the credentials expired
                try:
                    creds.refresh(Request())                                                    # refresh them from the token
                except RefreshError:
                    reload_needed = True
            else :                                                                          # otherwise
                reload_needed = True
            
            if not creds.scopes == SCOPES:
                reload_needed = True

            if reload_needed:
                store = file.Storage("Saved_Information/token.json")                        # grab or make the saved credentials token
                flow = client.flow_from_clientsecrets(                                      # authenticate manually
                    'Saved_Information/client_oauth.json', SCOPES
                )
                creds = tools.run_flow(flow, store)                                         # update the credentials from the manual authentication

            with open('Saved_Information/token.json', 'w') as token :                       # open 'tokens.json'
                token.write(creds.to_json())                                                # save the credentials to the json file


        sheet_service = discovery.build(                                                     # create the google api service for all future use
            "sheets",
            "v4",
            credentials=creds,
            # discoveryServiceUrl=DISCOVERY_DOC,
            # static_discovery=False,
        )

        return sheet_service
    


    def append(self, data : list):

        body = {'values': data}

        self.sheet_service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id, range="Sheet1!A1",
            valueInputOption="RAW", body=body).execute()