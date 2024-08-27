# from Function_Phases.Helpers import *

from Function_Phases.Information_Scraping import get_weekly_information
from Function_Phases.Initiation import send_out_initial_form
from Function_Phases.Confirmation import create_session_pairings

from Scheduled_Entities.Google_Sheet import Google_Sheet




def main():

    # get_weekly_information()

    # send_out_initial_form()

    # create_session_pairings()

    test = Google_Sheet("https://docs.google.com/spreadsheets/d/1ueTWu_qzz_CshyQsz3_J6j2yVMNs1mIqjJOmqu3KzC0/edit?gid=0#gid=0")
    test.append([[1,2,3], [4,5,6]])






    



main()