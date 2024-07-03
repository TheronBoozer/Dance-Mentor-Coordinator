import datetime
import time
import requests

from Timekeeping.Quarter_Hour import Quarter_Hour


class Twenty_Five_Live_Calendar:
    """
    Initialize with a 25Live location ID (located in the url of the 25live page)
    Stores the details page link, the ID, and an array of booked times
    """



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////*   INITIALIZER   *///////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, link : str):
        self.live_link = link                                                           # save the provided link
        find_id_link = link[link.find("location/")+9:]                                  # find the start of the id from the url
        self.id = int(find_id_link[:find_id_link.find("/")])                            # find the end of the id and save it
        self.update()                                                                   # find and save the booked times for the next week


    
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////*   PRIVATE METHODS   */////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __timestamp_to_week_tuple(self, timestamp : str) -> tuple :
        """
        Takes in the 25Live timestamp (`"20240225T070438/r"`) 
        Returns a tuple with the weekday and hour:minute unix timestamp (`(4, 70438)`)
        """

        full_unix = datetime.datetime.strptime(str(timestamp[:-1:]), "%Y%m%dT%H%M%S")   # get the full unix timestamp
        time_unix = int(time.mktime(full_unix.timetuple())) % (24*3600) - 4*3600        # convert the full unix to just the hour and minute in EST
        weekday = full_unix.weekday()                                                   # get the weekday from the full unix

        return (weekday, time_unix)
    

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////*   PUBLIC METHODS   *//////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def update(self):
        """
        Finds a list of unavailable quarter hours for the location
        Returns tuples in the format ('weekday', 'unix hours:minutes')
        """

        today = datetime.datetime.now()         # get todays date
        day_of_the_week = today.weekday()       # get todays weekday

        days_to_sunday = 7-day_of_the_week                  # convert todays weekday into the number of days until sunday (Mon-0, Sun-7)
        days_to_next_saturday = days_to_sunday + 6          # Add six days to find the following saturday

        calendar_page = requests.get(f"https://25live.collegenet.com/25live/data/wpi/run/rm_reservations.ics?caller=pro&space_id={self.id}&start_dt=+{days_to_sunday}&end_dt=+{days_to_next_saturday}&options=standard")
        calendar_text = calendar_page.text                  # convert it all to text
        calendar_data = calendar_text.split("\n")           # split the text around returns

        calendar_booked_times = []                                                  # create the empty array to be returned

        for data in calendar_data:                                                  # iterate through each calendar line

            if data.startswith("DTSTART;TZID=America/New_York:"):                   # check if the line is an event start time
                dt = data.removeprefix("DTSTART;TZID=America/New_York:")            # if so, remove the prefix
                start = self.__timestamp_to_week_tuple(dt)                          # set the start marker to that time

            elif data.startswith("DTEND;TZID=America/New_York:"):                   # check if the line is an event end time
                dt = data.removeprefix("DTEND;TZID=America/New_York:")              # if so, remove the prefix
                end = self.__timestamp_to_week_tuple(dt)                            # set the end time
                for i in range(start[1], end[1], 15*60):                            # iterate from the start marker until the end time by quarter hours
                    quarter = Quarter_Hour(start[0], i)                             # create Quarter_Hours object for the given time
                    calendar_booked_times.append(quarter)                           # add that quarter hour to the returned list

        self.booked_times = calendar_booked_times



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////*   GETTERS   */////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def get_unavailable_times(self):
        return self.booked_times
    


    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # /////////////////////////////////////////*   TO STRING   *////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __str__(self) -> str:
        return str([str(week_quarter) for week_quarter in self.booked_times]).replace('\\x1b', '\033')