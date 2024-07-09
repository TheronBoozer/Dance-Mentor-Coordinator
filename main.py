from Helpers import *




def main():
    
    mentor_dict = get_mentors()
    print(mentor_dict)

    location_dict = get_locations()
    print(location_dict)

    session_requests = get_sessions()
    print(session_requests)

    print(str(mentor_dict['Theron Boozer'].get_schedule()))
    print(str(location_dict['RC Dance Studio'].get_schedule()))
    print(str(session_requests[0].get_schedule()))




    # test = mentor_dict['Theron Boozer'].get_schedule().cross_check_with(location_dict['RC Dance Studio'].get_schedule())
    # print (len(test))





main()


