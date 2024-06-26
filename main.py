from Location import Location
from Mentor import Mentor
from Mentor import get_mentors
import requests



dance_mentor_information_sheet_link = 'https://docs.google.com/spreadsheets/d/1PXghhfh87fMG5kmgNM9Ld4PdWMautXA7h8l2KwUOKO4/edit?resourcekey=&gid=250951273#gid=250951273'


def main():
    test = Location(353, 7, 23)
    
    # mentor_list = get_mentors(dance_mentor_information_sheet_link)
    # for mentor in mentor_list:
    #     print(mentor)
    #     print('\n_______________________\n')


    test.get_name_and_hours()




main()