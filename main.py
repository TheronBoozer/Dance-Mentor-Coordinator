from Helpers import *




def main():
    send_out_initial_weekly_form()





def send_out_initial_weekly_form():

    mentor_list = get_mentors()

    location_list = get_locations()

    session_requests = get_sessions()

    form = make_initial_form(mentor_list, location_list, session_requests)

    form.update_responses()
    # send_form(form) TODO: test this
    
    
    
main()