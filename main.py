
from Scheduled_Entities.Google_Form import Google_Form
from Scheduler import assign_task_timing
import getpass
import os
from pathlib import Path



def main():

    print("it's go time")

    add_to_startup()
    assign_task_timing()


def add_to_startup(file_path=""):
    USER_NAME = getpass.getuser()
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    bat = Path(bat_path + "\\" + "DM_Bot.bat")

    if bat.exists():
        return
    
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    with open(bat_path + '\\' + "DM_bot.bat", "w+") as bat_file:
        bat_file.write(r'''@echo off
cd %s
python main.py
pause''' % file_path)


def update_tokens():
    Google_Form("https://docs.google.com/spreadsheets/d/1PtMRoHYLS_VMHVLC0O4lCinp1BIVL-425-z9owAa88U/edit?resourcekey=&gid=553428416#gid=553428416")


# update_tokens()
main()