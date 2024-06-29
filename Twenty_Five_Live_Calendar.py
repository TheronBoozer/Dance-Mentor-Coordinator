

import datetime
import time
from bs4 import BeautifulSoup
import requests


class Twenty_Five_Live_Calendar:
    live_link = ""
    id = 0

    def __init__(self, id : int):
        self.id = id
        self.live_link = f"https://25live.collegenet.com/pro/wpi#!/home/location/{id}/details"


    def get_booked_times(self):
        # print("calendar:")
        response = requests.get(f"https://25live.collegenet.com/25live/data/wpi/run/rm_reservations.ics?caller=pro&space_id={id}&start_dt=0&end_dt=+6&options=standard")
        soup = BeautifulSoup(response.text, "html.parser")
        soup.prettify

        cal_text = soup.text
        calendar_data = cal_text.split("\n")

        calendar_booked_times = []
        start = 0
        for data in calendar_data:
            if data.startswith("DTSTART;TZID=America/New_York:"):
                dt = data.removeprefix("DTSTART;TZID=America/New_York:")
                start = timestamp_to_unix(dt)

            elif data.startswith("DTEND;TZID=America/New_York:"):
                dt = data.removeprefix("DTEND;TZID=America/New_York:")
                end = timestamp_to_unix(dt)
                for i in range(start[1], end[1], 15*60):
                    calendar_booked_times.append((start[0], i))


        return calendar_booked_times
    


def timestamp_to_unix(timestamp : str) -> tuple :
    """Takes in the 25Live timestamp (`"20240225T070438/r"`) and converts it to unix timestamp (`1708862678`)"""
    full_unix = datetime.datetime.strptime(str(timestamp[:-1:]), "%Y%m%dT%H%M%S")
    time_unix = int(time.mktime(full_unix).timetuple()) % 24*3600
    weekday = full_unix.weekday()

    return (weekday, time_unix)