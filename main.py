from Phases.Information_Scraping import get_weekly_information
from Phases.Initiation import send_out_initial_form
from Phases.Confirmation import create_session_pairings
from Phases.Phase_Test import test
from Phases.Update import update
from Phases.Restart import reboot

import os
import sys


def main():
    """
    Adds the created tasks to the correctly scheduled times
    """

    print(f"running on: {os.name};\n\t - 'nt' = Windows\n\t - 'posix' = Linux\n\n")

    task = ''
    if len(sys.argv) > 1:
        task = sys.argv.pop(1)

    if task == "Scrape":

        get_weekly_information()
        print("Information saved as pickles (file format, not the food)")

    elif task == "Initiate":

        send_out_initial_form()
        print("Form edited with new sessions")
        print("Emails sent")
                

    elif task == "Confirm":

        create_session_pairings()
        print("Sessions paired between mentors and mentees")
        print("Emails sent")
                
    elif task == "Update":

        print("Updating...\nWill reboot soon")
        update()

    elif task == "Restart":

        print("Will reboot soon")
        reboot()

    else:
        print("Please enter a command line argument for what the program should do\n")

    test()
main()