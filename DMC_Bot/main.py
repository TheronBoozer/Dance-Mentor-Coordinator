from Function_Phases.Information_Scraping import get_weekly_information
from Function_Phases.Initiation import send_out_initial_form
from Function_Phases.Confirmation import create_session_pairings
from Function_Phases.Update import update

from Scheduled_Entities.Google_Form import Google_Form
from Scheduler import assign_task_timing
# import getpass
import os
# from pathlib import Path

from Scheduling.When2Meet import When2Meet
from Scheduling.Schedule import Schedule

def main():

    print("it's go time")
    print(f"running on: {os.name};\n\t - 'nt' = Windows\n\t - 'posix' = Linux\n")

    # add_to_startup()
    # assign_task_timing()
    get_weekly_information()
    send_out_initial_form()
    # update_tokens()
    create_session_pairings()
    # update()

    # tristen_when = When2Meet("https://www.when2meet.com/?26094819-wqXFj")
    # TEST_when = When2Meet("https://www.when2meet.com/?28104739-d8Spw")

    # tristen = Schedule().change_availability(tristen_when)
    # TEST = Schedule().change_availability(TEST_when)

    # combined = TEST.cross_check_with(tristen)

    # print(combined)




# def add_to_startup(file_path=""):

#     if(os.name == 'nt'):
#         USER_NAME = getpass.getuser()
#         bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\DM_Bot.bat' % USER_NAME
#         bat = Path(bat_path)
#     elif(os.name == 'posix'):
#         print("unsupported OS")
#         return
#     else:
#         bat_path = "/etc/init.d/DM_Bot.bat"
#         bat = Path(bat_path)


#     if bat.exists():
#         return
    
#     if file_path == "":
#         file_path = os.path.dirname(os.path.realpath(__file__))
#     with open(bat_path, "w+") as bat_file:
#         bat_file.write(r'''@echo off
# cd %s
# python main.py
# pause''' % file_path)


def update_tokens():
    Google_Form("https://docs.google.com/spreadsheets/d/1PtMRoHYLS_VMHVLC0O4lCinp1BIVL-425-z9owAa88U/edit?resourcekey=&gid=553428416#gid=553428416")


main()