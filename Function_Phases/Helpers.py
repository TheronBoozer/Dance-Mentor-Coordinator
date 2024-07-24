import datetime
import requests
import json



# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////*   PRIVATE METHODS   */////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////

def __remove_old_rows(rows : list):
    """
    A function that removes rows with a timestamp older than the last 'initial' phase
    """
    
    last_week_timing = weekly_timing("initiation")                                                      # get the unix timestamp of last weeks run

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

def get_links():
    """
    Fetches the links to the location and mentor google sheets
    """
    
    links = json.load(open('Saved_Information/links.json'))                                             # open the file 'links.json'
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


def weekly_timing(phase : str, last_week=True):
    """
    convert an array in the form ["weekday", hour, minute] into the unix timestamp of the past week
        set last_week to False to grab the most recent one
    """

    phase_time = json.load(open('Saved_Information/timing.json'))[phase]                                        # grab what time the program is meant to run each week

    weekday_reference = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]          # create a weekday reference array

    current_weekday = datetime.datetime.now().weekday()                                                         # get what weekday it is today
    target_weekday = weekday_reference.index(phase_time[0].capitalize())                                        # convert the weekday string to the numeric interpretation

    current_time = int(datetime.datetime.now().timestamp())                                                     # get the current timestamp
    target_hour = phase_time[1]                                                                                 # save the target hour in military time
    target_minute = phase_time[2]                                                                               # save the target minute

    days_between_target_and_now = (current_weekday + (7 - target_weekday)) % 7 + 7 * int(last_week)             # some math to find how many days have passed since the target day

    target_day = current_time - days_between_target_and_now * 24 * 3600                                         # get to the correct unix day
    target_time = target_day - target_day % (24*3600) - 4*3600 + target_hour*3600 + target_minute*60            # remove any residual time then add to get back to the target including fixing for timezones

    return target_time