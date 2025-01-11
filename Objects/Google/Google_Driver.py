from apiclient import discovery
from oauth2client import client, file, tools
from oauth2client.service_account import ServiceAccountCredentials

import os.path
import httplib2

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from file_paths import SERVICE_AUTH, CLIENT_AUTH, AUTH_TOKEN



SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/forms.responses.readonly']
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

class Google_Driver:

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////*   INITIALIZER   *///////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, link : str):

        start_index = link.find('/d/') + 3                              # find the start of the form ID

        self.id = link[start_index:link.rindex('/')]               # clip the id out of the url





    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////*   PRIVATE METHODS   */////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __setup_from_service_account(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_AUTH, SCOPES)

        if not creds or creds.invalid:
            print("unable to authenticate using service key")
            return
            
        return creds.authorize(httplib2.Http())
        

    def setup_form_service(self):
        http_auth = self.__setup_from_service_account()
        
        return discovery.build(
            'forms',
            'v1',
            http=http_auth
        )
    
    def setup_sheet_service(self):
        http_auth = self.__setup_from_service_account()
        
        return discovery.build(
            'sheets',
            'v4',
            http=http_auth
        )