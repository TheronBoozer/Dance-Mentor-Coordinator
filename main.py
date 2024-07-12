from Google_Form import Google_Form
from Helpers import *




def main():
    # print(get_sessions())
    form = Google_Form('https://docs.google.com/forms/d/1S0D8c-8_oXHXEF687RoDfXnxxnqM9ZLXJHNiLlparqo/edit')

    form.clear_form()
    # form.add_section("1", "teehee")
    # form.add_section("2", "haha")
    # form.add_section("3", "heeheehaha")
    # form.add_multiple_choice_question("Question:", "A silly little question", ["1", "2", "3"], "DROP_DOWN", section_selection=True)




def setup():
    mentor_dict = get_mentors()

    location_dict = get_locations()

    session_requests = get_sessions()


main()


