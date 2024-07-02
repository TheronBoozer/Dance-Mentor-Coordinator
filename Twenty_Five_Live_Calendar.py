import datetime
import time
import requests


class Twenty_Five_Live_Calendar:
    live_link = ""      # details page link
    id = 0              # 25Live location ID number used in every link corresponding to that location

    def __init__(self, id : int):
        self.id = id
        self.live_link = f"https://25live.collegenet.com/pro/wpi#!/home/location/{id}/details"


    def get_booked_times(self):
        """Returns a list of unavailable quarter hours for the location in tuples in the format ('weekday', 'unix hours:minutes')"""

        today = datetime.datetime.now()         # get todays date
        day_of_the_week = today.weekday()       # get todays weekday

        days_to_sunday = 6-day_of_the_week if not day_of_the_week == 0 else 0   # convert todays weekday into the number of days until sunday (0 if it already is sunday)
        days_to_next_saturday = days_to_sunday + 6                              # Add six days to find the following saturday

        calendar_page = requests.get(f"https://25live.collegenet.com/25live/data/wpi/run/rm_reservations.ics?caller=pro&space_id={self.id}&start_dt=+{days_to_sunday}&end_dt=+{days_to_next_saturday}&options=standard")
        calendar_text = calendar_page.text                  # convert it all to text
        calendar_data = calendar_text.split("\n")           # split the text around returns

        calendar_booked_times = []                                                  # create the empty array to be returned

        for data in calendar_data:                                                  # iterate through each calendar line

            if data.startswith("DTSTART;TZID=America/New_York:"):                   # check if the line is an event start time
                dt = data.removeprefix("DTSTART;TZID=America/New_York:")            # if so, remove the prefix
                start = timestamp_to_unix(dt)                                       # set the start marker to that time

            elif data.startswith("DTEND;TZID=America/New_York:"):                   # check if the line is an event end time
                dt = data.removeprefix("DTEND;TZID=America/New_York:")              # if so, remove the prefix
                end = timestamp_to_unix(dt)                                         # set the end time
                for i in range(start[1], end[1], 15*60):                            # iterate from the start marker until the end time by quarter hours
                    calendar_booked_times.append((start[0], i))                     # add that quarter hour to the returned list along with its weekday


        return calendar_booked_times                        # return
    


def timestamp_to_unix(timestamp : str) -> tuple :
    """Takes in the 25Live timestamp (`"20240225T070438/r"`) and converts it to a tuple with the weekday and hour:minute unix timestamp (`(4, 70438)`)"""

    full_unix = datetime.datetime.strptime(str(timestamp[:-1:]), "%Y%m%dT%H%M%S")   # get the full unix timestamp
    time_unix = int(time.mktime(full_unix.timetuple())) % (24*3600) - 4*3600        # convert the full unix to just the hour and minute in EST
    weekday = full_unix.weekday()                                                   # get the weekday from the full unix

    return (weekday, time_unix)