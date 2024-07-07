from Scheduling.Twenty_Five_Live_Calendar import Twenty_Five_Live_Calendar
from Scheduling.When2Meet import When2Meet
from Scheduling import Schedule

from Timekeeping.Day import Day


class Schedule:
    """
    A container for seven days with methods to cvhange availability by quarter hours
    """
    


    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////*   INITIALIZER   *///////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self):
        self.calendar = [Day(i) for i in range(7)]                          # set calendar to have 7 days for each day of the week
        self.free_hours = self.__update_free_hours()



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////*   PRIVATE METHODS   */////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __update_free_hours(self):
        """
        Return the available hours of the schedule
        """

        free_hours = []                                     # create returnable array of hours
        for day in self.calendar:                           # for each day in the calendar
            free_hours.extend(day.find_free_hours())             # add the avalable hours

        return free_hours
    


    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////*   PUBLIC METHODS   */////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def change_availability(self, when2meet_calendar : When2Meet):
        """
        Sets the given When2Meet quarters to be available in the calendar
        takes in a When2Meet object
        """
        
        available_quarters = when2meet_calendar.get_availability()                      # get the array of available quarters from the When2Meet

        for quarter in available_quarters:                                                                                                              # for each quarter in the available ones 
            self.calendar[quarter.get_weekday()].get_quarters()[int(quarter.get_start_time().get_int_time() / (15*60))].set_available()                 # change the corresponding quarter in the calendar to be available
        
        self.free_hours = self.__update_free_hours()                                    # update the hours of availability

        return self                                                                     # return self for convenience
    

    def change_unavailability(self, live_calendar : Twenty_Five_Live_Calendar):
        """
        Sets the given 25Live quarters to be available in the calendar
        takes in a Twenty_Five_Live_Calendar object
        """
        
        unavailable_quarters = live_calendar.get_unavailable_times()                    # get the array of booked quarters from 25Live
        for quarter in unavailable_quarters:                                                                                                            # for each quarter in the unavailable ones
            self.calendar[quarter.get_weekday()].get_quarters()[int(quarter.get_start_time().get_int_time() / (15*60))].set_unavailable()               # change the corresponding quarter in the calendar to be unavailable
        
        self.free_hours = self.__update_free_hours()                                    # update the hours of availability

        return self                                                                     # return self for convenience
    

    def cross_check_with(self, other : Schedule):
        print(str(self))
        print(str(other))
        combined_hours = []
        for hour in self.free_hours:
            # for other_hour in other.free_hours:
            #     if hour == other_hour:

            if hour in other.get_free_hours():
                    combined_hours.append(hour)

        return combined_hours



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////*   GETTERS   */////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def get_free_hours(self):
        return self.free_hours



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # /////////////////////////////////////////*   TO STRING   *////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __str__(self) -> str:
        returnable_str = ""                                                 # start with an empty string to add to

        for day in self.calendar:                                           # for every day in the calendar
            returnable_str = f"{returnable_str}\n\n{str(day)}"              # return and then add that day to the string

        returnable_str = returnable_str[2:]                                 # cut off the first two returns

        return returnable_str                                               # return the new built up string

