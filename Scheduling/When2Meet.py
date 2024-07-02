# date and time handling imports
import datetime
import time

# html parsing imports
import re
from bs4 import BeautifulSoup
import requests

# from Timekeeping
from Timekeeping.Quarter_Hour import Quarter_Hour
from Timekeeping.Week_Quarter_Hour import Week_Quarter_Hour


class When2Meet:
    """
    Initialize with the When2Meet link
    Stores the link and an array designating each available time
    """

    link = ""                                       # link to the when2meet
    available_quarter_hours = []                    # array of tuples containing weekday, Quarter_Hour EX: Thursday at 1:30 pm --> (3, )

    # Initializer
    def __init__(self, link):
        self.link = link                            # store the link
        self.update()                               # find and save the available times


    # Private Methods
    def __unix_to_week_tuple(self, timestamp : str) -> tuple :
        """
        Takes in the 25Live timestamp (`"20240225T070438/r"`) 
        Returns a tuple with the weekday and hour:minute unix timestamp (`(4, 70438)`)
        """

        full_unix = datetime.datetime.fromtimestamp(int(timestamp))
        time_unix = int(time.mktime(full_unix.timetuple())) % (24*3600) - 4*3600        # convert the full unix to just the hour and minute in EST
        weekday = full_unix.weekday()                                                   # get the weekday from the full unix
        quarter = Quarter_Hour(time_unix)                                               # create Quarter_Hour object for the time
        weekly_quarter = Week_Quarter_Hour(weekday, quarter)

        return weekly_quarter
    

    def __green_block_style(self, style):
        """
        Used to identify all person availabilities on when2meet html pages
        Input for a BeautifulSoup object's .find_all(style=)
        """
        
        return style and re.compile("background: #339900;").search(style)               # finds all html objects with a background correlating to that of a when2meet available spot
    

    # Public Methods
    def update(self):
        """
        Finds a list of available quarter hours for the location
        Returns tuples in the format ('weekday', 'unix hours:minutes')
        """
        
        calendar_page = requests.get(self.link)                                                         # get the linked when2meet page
        calendar_html = BeautifulSoup(calendar_page.text, "html.parser")                                # parse the html with BeautifulSoup

        available_quarter_hour_html = calendar_html.find_all(style=self.__green_block_style)            # finds all free quarter hours in the pages html
        self.available_quarter_hours.clear()                                                            # clears any current available hours

        for quarter in available_quarter_hour_html:                                                     # loop through each available html 
            week_tuple = self.__unix_to_week_tuple(quarter["data-time"])                                # convert the unix time available to a tuple in the format of -> (weekday, time)
            self.available_quarter_hours.append(week_tuple)                                             # add the above tuple to the stored array of available times


    # Setters
    def set_link(self, link):
        self.link = link

    # Getters
    def get_availability(self):
        return self.available_quarter_hours
    
    # To String
    def __str__(self) -> str:
        return str([str(week_quarter) for week_quarter in self.available_quarter_hours]).replace('\\x1b', '\033')
