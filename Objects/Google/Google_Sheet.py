

from Objects.Google.Google_Driver import Google_Driver
from flags import *

import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery
from oauth2client import client, file, tools

import os.path
import httplib2

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from file_paths import AUTH_TOKEN, CLIENT_AUTH


SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/forms']

class Google_Sheet(Google_Driver):
    """
    Creates an editable google sheet object
    """
    


    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////*   INITIALIZER   *///////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, link : str):

        super().__init__(link)
        self.service = super().setup_sheet_service()
    

    def append(self, data : list):

        body = {'values': data}

        self.service.spreadsheets().values().append(
            spreadsheetId=self.id, range="Sheet1!A1",
            valueInputOption="RAW", body=body).execute()
        