import datetime
import pickle
import requests
import json
import smtplib

from file_paths import LINKS_FILE, SMTP_INFORMATION

# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////*   PRIVATE METHODS   */////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////

def __remove_old_rows(rows : list):
    """
    A function that removes rows with a timestamp older than the last 'initial' phase
    """
    
    last_week_timing = weekly_timing(["Saturday", "08:00"])                                                # get the unix timestamp of last weeks run

    for row in rows[::-1]:                                                                              # loop throw each row from the back
        fixed_format = row[:row.index("\t")].strip()                                                    # grab just the timestamp
        timestamp = datetime.datetime.strptime(fixed_format, "%m/%d/%Y %H:%M:%S").timestamp()           # create the integer timestamp from the readable one

        if int(timestamp) <  last_week_timing:                                                          # if the timestamp is older than last saturday
            rows = rows[rows.index(row)+1:]                                                             # clip the row array to only hold those more recent ones
            break

    return rows



# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////*   PUBLIC METHODS   */////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////

# --------------------------------------------
# -----------spreadsheet functions------------
# --------------------------------------------

def get_links():
    """
    Fetches the links to the location and mentor google sheets
    """
    
    links = json.load(open(LINKS_FILE))                                             # open the file 'links.json'
    return links                                                                                        # returns the dictionary


def create_2d_array(link : str, recent = False):
    """
    Generates a 2d array from a given google sheet link
    """
    
    csv_link = link[:link.index('edit')] + 'export?format=tsv'                                          # converts basic 'share' link to a readable csv link

    google_sheet = requests.get(csv_link)                                                               # read the csv file made from the link
    unorganized_data = google_sheet.text                                                                # sorts it into only the text
    array_of_str_rows = unorganized_data.split('\r')                                                    # splits the text into rows

    array_of_str_rows.pop(0)                                                                            # remove the label row


    if recent:                                                                                          # if only the recent rows are requested
        array_of_str_rows = __remove_old_rows(array_of_str_rows)                                        # remove the old ones
            

    sheet_information = []                                                                              # create empty array to be filled with row arrays 

    for str_row in array_of_str_rows:                                                                   # for each string
        row_array = str_row.split('\t')                                                                 # split the row text by commas
        row_array.pop(0)                                                                                # delete the timestamp
        sheet_information.append(row_array)                                                             # add to the master array



    return sheet_information


# --------------------------------------------
# ---------------docs functions---------------
# --------------------------------------------

def grab_text(link : str):
    txt_link = link[:link.index('edit')] + 'export?format=txt'                                          # converts basic 'share' link to a readable txt link

    google_doc = requests.get(txt_link)                                                                 # read the txt file made from the link
    text = google_doc.text                                                                              # sorts it into only the text

    return text


# --------------------------------------------
# --------------timing functions--------------
# --------------------------------------------

def weekly_timing(phase : list, last_week=True):
    """
    convert an array in the form ["weekday", hour, minute] into the unix timestamp of the past week
        set last_week to False to grab the most recent one
    """


    weekday_reference = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]          # create a weekday reference array

    current_weekday = datetime.datetime.now().weekday()                                                         # get what weekday it is today
    target_weekday = weekday_reference.index(phase[0].capitalize())                                        # convert the weekday string to the numeric interpretation

    current_time = int(datetime.datetime.now().timestamp())                                                     # get the current timestamp
    target_hour = int(phase[1][:phase[1].index(':')])                                                 # save the target hour in military time
    target_minute = int(phase[1][phase[1].index(':')+1:])                                             # save the target minute

    days_between_target_and_now = (current_weekday + (7 - target_weekday)) % 7 + 7 * int(last_week)             # some math to find how many days have passed since the target day

    target_day = current_time - days_between_target_and_now * 24 * 3600                                         # get to the correct unix day
    target_time = target_day - target_day % (24*3600) + 5*3600 + target_hour*3600 + target_minute*60            # remove any residual time then add to get back to the target including fixing for timezones

    return target_time


def weekday_to_date(weekday : str) -> str:
    """
    given a weekday this will return the next upcoming day with the correspoinding weekday
    """

    weekday_reference = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]          # create a weekday reference array
    current_timestamp = int(datetime.datetime.now().timestamp())-4*3600                                         # get the current timestamp accounting for timezones
    current_datetime = datetime.datetime.fromtimestamp(current_timestamp)

    current_weekday = current_datetime.weekday()                                                                # get what weekday it is today
    target_weekday = weekday_reference.index(weekday.capitalize())                                              # convert the weekday string to the numeric interpretation

    days_between_target_and_now = (target_weekday-current_weekday)%7
    target_timestamp = current_timestamp + days_between_target_and_now*24*3600
    target_datetime = datetime.datetime.fromtimestamp(target_timestamp)

    month = target_datetime.strftime("%B")
    day = target_datetime.strftime("%d")
    day = remove_padding(day)

    if day == '1' or day == '21' or day == '31':
        suffix = 'st'
    elif day == '2' or day == '22':
        suffix = 'nd'
    elif day == '3' or day == '23':
        suffix = 'rd'
    else:
        suffix = 'th'

    return f'{month} {day}{suffix}'


def remove_padding(padded_number : str) -> str:
    if padded_number.startswith('0'):
        return remove_padding(padded_number[1:])
    
    return padded_number


# --------------------------------------------
# --------------pickle functions--------------
# --------------------------------------------

def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

def recycle_object(filename):
    with open(filename, 'rb') as inp:
        return pickle.load(inp)
    

# --------------------------------------------
# --------------email functions---------------
# --------------------------------------------

def smtp_mailing(recipients, subject, body):
    smtp_info = json.load(open(SMTP_INFORMATION))['OUTLOOK']
    
    server = smtp_info['server']
    port = smtp_info['port']
    username = smtp_info['username']
    password = smtp_info['password']

    from_user = username
    to_user = ";".join(recipients)

    message = f'Subject: {subject}\n\n{body}'

    with smtplib.SMTP(server, port) as smtp:
        smtp.starttls()
        smtp.login(username, password)
        smtp.sendmail(from_user, to_user, message)