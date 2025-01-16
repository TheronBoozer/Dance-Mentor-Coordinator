# internal references
from Globals.Helpers import get_links, recycle_object
from Objects.Google.Google_Sheet import Google_Sheet
from Phases.Restart import reboot

from Globals.file_paths import SESSION_LOG

def update():

    count_sessions()

    reboot()


def count_sessions():

    sheet_link = get_links()["SESSION_LOG_SHEET"]

    sheet = Google_Sheet(sheet_link)

    session_log = recycle_object(SESSION_LOG)

    sheet.append(session_log)