###################################################
############### FILE PATHS ########################
###################################################

# folders
__PRIMARY_FOLDER = "Saved_Information/"

__IGNORED_FOLDER = __PRIMARY_FOLDER + "Ignored/"

__PICKLED_FOLDER = __PRIMARY_FOLDER + "Pickles/"


# files
EXPRESSIONS_FILE = __PRIMARY_FOLDER + "expressions.json"
LINKS_FILE = __PRIMARY_FOLDER + "links.json"
FORM_EMAIL = __PRIMARY_FOLDER + "Initial_Mentor_Email.txt"
REJECTION_EMAIL = __PRIMARY_FOLDER + "Rejection_Email.txt"
SESSION_EMAIL = __PRIMARY_FOLDER + "Secondary_Email_Confirmation.txt"

SAVED_OBJECTS = __PICKLED_FOLDER + "Scheduled_Entities.pkl"
SESSION_LOG = __PICKLED_FOLDER + "Session_Log.pkl"

CLIENT_AUTH = __IGNORED_FOLDER + "client_oauth.json"
SERVICE_AUTH = __IGNORED_FOLDER + "service_oauth.json"
SMTP_INFORMATION = __IGNORED_FOLDER + "smtp_secrets.json"
AUTH_TOKEN = __IGNORED_FOLDER + "token.json"