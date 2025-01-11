from apiclient import discovery
import httplib2
from oauth2client import client, file, tools
from oauth2client.service_account import ServiceAccountCredentials

import os.path

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from flags import *
from Function_Phases.Helpers import get_links




SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/forms']

class Google_Sheet:
    """
    Creates an editable google sheet object
    """
    


    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////*   INITIALIZER   *///////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, link : str, manual=False):

        start_index = link.find('/d/') + 3                              # find the start of the sheet ID

        self.sheet_id = link[start_index:link.rindex('/')]              # clip the id out of the url

        if manual:
            self.sheet_service = self.__setup_sheet_service()
        else:
            try:
                self.sheet_service = self.__setup_sheet_service()
            except:
                self.sheet_service = self.__setup_sheet_service_account()       # set up the sheet recognition and such



    def __setup_sheet_service_account(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name("DMC_Bot/Saved_Information/service_oauth.json", SCOPES)

        if not creds or creds.invalid:
            print("unable to authenticate using service key")
            return
            
        http_auth = creds.authorize(httplib2.Http())
        return discovery.build(
            'sheets',
            'v4',
            http=http_auth
        )

    def __setup_sheet_service(self):
        """
        Sets up the authentication for the sheet in question
        If not previously authenticated, the setup will need to be manually verified
        """
        
        creds = None                                                                        # create credentials
        reload_needed = False

        if os.path.exists("DMC_Bot/Saved_Information/token.json") :                                                   # if the file 'token.json' exists
            creds = Credentials.from_authorized_user_file('DMC_Bot/Saved_Information/token.json')             # make credentials from the saved token

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
                store = file.Storage("DMC_Bot/Saved_Information/token.json")                        # grab or make the saved credentials token
                flow = client.flow_from_clientsecrets(                                      # authenticate manually
                    'DMC_Bot/Saved_Information/client_oauth.json', SCOPES
                )
                creds = tools.run_flow(flow, store)                                         # update the credentials from the manual authentication
            with open('DMC_Bot/Saved_Information/token.json', 'w') as token :                       # open 'tokens.json'
                token.write(creds.to_json())                                                # save the credentials to the json file


        sheet_service = discovery.build(                                                     # create the google api service for all future use
            "sheets",
            "v4",
            credentials=creds,
        )

        return sheet_service
    


    def append(self, data : list):

        body = {'values': data}

        self.sheet_service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id, range="Sheet1!A1",
            valueInputOption="RAW", body=body).execute()
        



def authenticate_google():
    #try:
        link = get_links()["CONFIRMATION_FORM_EDIT_LINK"]
        Google_Sheet(link, manual=True)
        if DEBUG_ON:
            print(f"Authentication credentials updated with the following scopes:\n\t{', '.join(SCOPES)}")
    #exc#nt("Failed to authenticate credentials.\nPlease try again and follow the link to provide access to your google sheets and forms.")