from Function_Phases.Information_Scraping import get_weekly_information
from Function_Phases.Initiation import send_out_initial_form
from Function_Phases.Confirmation import create_session_pairings
from Function_Phases.Update import update
from Function_Phases.Restart import reboot

from Scheduler import assign_task_timing
import os
import sys


def main():
    """
    Adds the created tasks to the correctly scheduled times
    """

    print("it's go time")
    print(f"running on: {os.name};\n\t - 'nt' = Windows\n\t - 'posix' = Linux\n")

    task = sys.argv[0]

    if task == "Schedule":
        assign_task_timing()
    elif task == "Scrape":
        get_weekly_information()
    elif task == "Initiate":
        send_out_initial_form()
    elif task == "Confirm":
        create_session_pairings()
    elif task == "Update":
        update()
    elif task == "Restart":
        reboot()
    else:
        print("Please enter a command line argument for what the program should do/n")




main()