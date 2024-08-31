
# from Function_Phases.Information_Scraping import get_weekly_information
# from Function_Phases.Initiation import send_out_initial_form
# from Function_Phases.Confirmation import create_session_pairings

from Scheduler import assign_task_timing
from Function_Phases.Helpers import add_to_startup



def main():

    # get_weekly_information()

    # send_out_initial_form()

    # create_session_pairings()
    add_to_startup()
    assign_task_timing()





main()