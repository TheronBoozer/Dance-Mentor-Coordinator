from Function_Phases.Information_Scraping import get_weekly_information
from Function_Phases.Initiation import send_out_initial_form
from Function_Phases.Confirmation import create_session_pairings
from Function_Phases.Update import update

from Scheduler import assign_task_timing
import os


def main():
    """
    Adds the created tasks to the correctly scheduled times
    """
    
    print("it's go time")
    print(f"running on: {os.name};\n\t - 'nt' = Windows\n\t - 'posix' = Linux\n")

    assign_task_timing()
    # get_weekly_information()
    # send_out_initial_form()
    # create_session_pairings()
    # update()




main()