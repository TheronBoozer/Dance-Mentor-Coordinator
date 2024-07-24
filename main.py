from Function_Phases.Helpers import *

from Function_Phases.Information_Scraping import get_weekly_information
from Function_Phases.Initiation import send_out_initial_form
from Function_Phases.Confirmation import create_session_pairings




def main():

    weekly_information = get_weekly_information()

    confirmation_form = send_out_initial_form(weekly_information)

    create_session_pairings(weekly_information, confirmation_form)









    
    
main()