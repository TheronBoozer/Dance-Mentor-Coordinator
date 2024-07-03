from Scheduling.Schedule import Schedule
from Scheduling.Twenty_Five_Live_Calendar import Twenty_Five_Live_Calendar
from Scheduling.When2Meet import When2Meet



class Location:
    """
    An object to store practice location information such as the locations schedule
    """



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////*   INITIALIZER   *///////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, information):
        self.name = information[0]                                                          # store the location name
        self.schedule = Schedule()                                                          # create a base schedule

        self.twenty_five_live_link = information[1]                                         # save 25live link
        self.when2meet_link = information[2]                                                # save when2meet link

        self.booked_quarters = Twenty_Five_Live_Calendar(self.twenty_five_live_link)        # save the booked times according to 25live
        self.available_quarters = When2Meet(self.when2meet_link)                            # save the available times according to a when2meet

        self.schedule.change_availability(self.available_quarters)                          # update the schedule with the available times
        self.schedule.change_unavailability(self.booked_quarters)                           # update the schedule with the unavailable times



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # /////////////////////////////////////////*   TO STRING   *////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __str__(self) -> str:
        return f"""
    {self.name}:
     Operating Hours - {self.when2meet_link}
     25Live page - {self.twenty_five_live_link}
                """
