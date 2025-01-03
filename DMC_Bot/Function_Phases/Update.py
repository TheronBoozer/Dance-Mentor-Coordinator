# internal references
from Function_Phases.Helpers import get_links, recycle_object
from Scheduled_Entities.Google_Sheet import Google_Sheet
from Function_Phases.Restart import reboot

# run foremost function
from Function_Phases.Update import update
update()


def update():

    count_sessions()

    update_saved_info()

    reboot()


def count_sessions():

    sheet_link = get_links()["SESSION_LOG_SHEET"]

    sheet = Google_Sheet(sheet_link)

    session_log = recycle_object('DMC_Bot/Saved_Information/Session_Log.pkl')

    sheet.append(session_log)

def update_saved_info():
    return