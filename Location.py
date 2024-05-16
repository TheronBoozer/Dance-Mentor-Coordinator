import math
import requests
from bs4 import BeautifulSoup
from Schedule import Schedule
from Helpers import *

class Location:
    id = 353     #353 is the dance studio
    schedule = Schedule()

    def __init__(self, space_id):
        self.id = space_id

    
    def get_start_end_times(self):
        print("calendar:")
        response = requests.get("https://25live.collegenet.com/25live/data/wpi/run/rm_reservations.ics?caller=pro&space_id={}&start_dt=0&end_dt=+6&options=standard".format(self.id))
        soup = BeautifulSoup(response.text, "html.parser")
        soup.prettify

        cal_text = soup.text
        cal_data = cal_text.split("\n")

        cal_times = []
        for data in cal_data:
            if data.startswith("DTSTART;TZID=America/New_York:"):
                dt = data.removeprefix("DTSTART;TZID=America/New_York:")

            elif data.startswith("DTEND;TZID=America/New_York:"):
                dt = data.removeprefix("DTEND;TZID=America/New_York:")

            else:
                continue
            
            dt = timestamp_to_unix(dt)
            cal_times.append(dt)

        
        # print(cal_times)
        return cal_times


    def set_schedule(self):
        start_end_times = self.get_start_end_times()
        is_end_time = False
        calendar = self.schedule.reset_calendar_bookings()
        for dt in start_end_times:
            day = datetime.datetime.fromtimestamp(dt).strftime("%w")
            print(day)
            

