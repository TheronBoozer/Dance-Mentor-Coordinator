from Day import Day
from Location import Location
from Mentor import Mentor
from Mentor import get_mentors
import requests

from Twenty_Five_Live_Calendar import Twenty_Five_Live_Calendar



dance_mentor_information_sheet_link = 'https://docs.google.com/spreadsheets/d/1PXghhfh87fMG5kmgNM9Ld4PdWMautXA7h8l2KwUOKO4/edit?resourcekey=&gid=250951273#gid=250951273'


def main():
    # test = Location(353, 7, 23)
    
    # mentor_list = get_mentors(dance_mentor_information_sheet_link)
    # for mentor in mentor_list:
    #     print(mentor)
    #     print('\n_______________________\n')

    # day = Day(2)
    # print(day)
    # test = [i*15 for i in range(96)]

    # print(test)
    live = Twenty_Five_Live_Calendar(353)

    print(live.get_booked_times())





main()