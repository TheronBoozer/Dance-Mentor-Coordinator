from Timekeeping.Day import Day
from People_and_places.Location import Location
from People_and_places.Mentor import Mentor
from People_and_places.Mentor import get_mentors
import requests

from Timekeeping.Quarter_Hour import Quarter_Hour
from Scheduling.Twenty_Five_Live_Calendar import Twenty_Five_Live_Calendar
from Scheduling.When2Meet import When2Meet



DANCE_MENTOR_INFORMATION_SHEET_LINK = 'https://docs.google.com/spreadsheets/d/1PXghhfh87fMG5kmgNM9Ld4PdWMautXA7h8l2KwUOKO4/edit?resourcekey=&gid=250951273#gid=250951273'
LOCATION_INFORMATION_SHEET_LINK = "https://docs.google.com/spreadsheets/d/1L2Plgoly26nA3JbeQHk6si435xnZJkBeNMDg_CqHEaw/edit?resourcekey=&gid=1306915179#gid=1306915179"



def main():
    # test = Location(353, 7, 23)
    
    # mentor_list = get_mentors(DANCE_MENTOR_INFORMATION_SHEET_LINK)
    # for mentor in mentor_list:
    #     print(mentor)
    #     print('\n_______________________\n')

    # day = Day(2)
    # print(day)
    # test = [i*15 for i in range(96)]

    # print(test)
    # live = Twenty_Five_Live_Calendar(353)

    # print(live.get_booked_times())

    meet = When2Meet("https://www.when2meet.com/?25385191-pFD1g")
    print(meet)

    live = Twenty_Five_Live_Calendar(353)
    print(live)





main()