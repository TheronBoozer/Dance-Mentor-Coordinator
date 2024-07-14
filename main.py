from Helpers import *




def main():

    mentor_list = get_mentors()

    location_list = get_locations()

    session_requests = get_sessions()

    form = make_initial_form(mentor_list, location_list, session_requests)

    




main()


