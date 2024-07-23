from Helpers import *




def main():
    print(weekly_timing(["monday", 2, 0]))
    # weekly_information = get_weekly_information()

    # confirmation_form = send_out_initial_form(weekly_information)

    # create_session_pairings(weekly_information, confirmation_form)


def get_weekly_information():

    information = {
        "mentor_list" : get_mentors(),
        "location_list" : get_locations(),
        "session_requests" : get_sessions(),
    }

    return information


def send_out_initial_form(info) -> Google_Form:

    mentor_list = info["mentor_list"]

    location_list = info["location_list"]

    session_requests = info["session_requests"]

    form = make_initial_form(mentor_list, location_list, session_requests)

    # send_form(form) TODO: test this
    
    return form


def create_session_pairings(info, form : Google_Form):

    mentor_list = info["mentor_list"]

    location_list = info["location_list"]

    session_requests = info["session_requests"]

    form.update_responses()
    
    
main()