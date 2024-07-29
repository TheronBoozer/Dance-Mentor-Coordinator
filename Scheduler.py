import time
import schedule

from Function_Phases.Information_Scraping import get_weekly_information
from Function_Phases.Initiation import send_out_initial_form
from Function_Phases.Confirmation import create_session_pairings


def assign_task_timing():
    # Run job on a specific day of the week
    schedule.every().friday.at("23:45").do(job)

    # Run job on a specific day of the week and time
    schedule.every().friday.at("13:15").do(job)

    

    while True:
        schedule.run_pending()
        time.sleep(1800)