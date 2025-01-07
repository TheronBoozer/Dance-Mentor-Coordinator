from Scheduled_Entities.Google_Sheet import authenticate_google
from Function_Phases.Information_Scraping import get_weekly_information
from Function_Phases.Initiation import send_out_initial_form
from Function_Phases.Confirmation import create_session_pairings
from Function_Phases.Update import update
from Function_Phases.Restart import reboot
from Scheduler import assign_task_timing
from flags import *

import os
import sys


def main():
    """
    Adds the created tasks to the correctly scheduled times
    """

    if DEBUG_ON:
        print("it's go time")
        print(f"running on: {os.name};\n\t - 'nt' = Windows\n\t - 'posix' = Linux\n\n")

    task = sys.argv.pop(1)

    if task == "Schedule":
        
        if DEBUG_ON: print("Assigning tasks\n Beginning while(true) loop")
        assign_task_timing()
        if DEBUG_ON: print("forever loop exited for unknown reason")

    elif task == "Scrape":

        get_weekly_information()
        if DEBUG_ON: print("Information saved as pickles (file format, not the food)")

    elif task == "Initiate":

        send_out_initial_form()
        if DEBUG_ON: print("Form edited with new sessions")
        if DEBUG_ON and EMAIL_ON: print("Emails sent")
                

    elif task == "Confirm":

        create_session_pairings()
        if DEBUG_ON: print("Sessions paired between mentors and mentees")
        if DEBUG_ON and EMAIL_ON: print("Emails sent")
                
    elif task == "Update":

        if DEBUG_ON: print("Updating...\nWill reboot soon")
        update()

    elif task == "Restart":

        if DEBUG_ON: print("Will reboot soon")
        reboot()

    elif task == "Authenticate":

        authenticate_google()

    else:
        print("Please enter a command line argument for what the program should do\n")




main()