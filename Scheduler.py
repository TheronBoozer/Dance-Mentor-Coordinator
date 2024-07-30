import json
import time
import schedule

from Function_Phases.Information_Scraping import get_weekly_information
from Function_Phases.Initiation import send_out_initial_form
from Function_Phases.Confirmation import create_session_pairings


def assign_task_timing():
    # Run job on a specific day of the week
    assign_timing("setup", get_weekly_information)

    assign_timing("initiation", send_out_initial_form)

    assign_timing("confirmation", create_session_pairings)

    

    while True:
        schedule.run_pending()
        time.sleep(1800)


def assign_timing(phase : str, function : function):
    weektime = json.load(open('Saved_Information/timing.json'))[phase]

    weekday = weektime[0]
    time = weektime[1]

    match(weekday.capitalize()):
        case "Monday":
            schedule.every().monday.at(time).do(function)
        case "Tuesday":
            schedule.every().tuesday.at(time).do(function)
        case "Wednesday":
            schedule.every().wednesday.at(time).do(function)
        case "Thursday":
            schedule.every().thursday.at(time).do(function)
        case "Friday":
            schedule.every().friday.at(time).do(function)
        case "Saturday":
            schedule.every().saturday.at(time).do(function)
        case "Sunday":
            schedule.every().sunday.at(time).do(function)
