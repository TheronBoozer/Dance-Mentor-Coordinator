from Helpers import *




def main():

    mentor_list = get_mentors()

    location_list = get_locations()

    session_requests = get_sessions()

    form = make_initial_form(mentor_list, location_list, session_requests)

    # test = Google_Form("https://docs.google.com/forms/d/1S0D8c-8_oXHXEF687RoDfXnxxnqM9ZLXJHNiLlparqo/edit")
    # test.clear_form()
    # test.add_section("hello", None)
    




main()


