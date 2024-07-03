from typing import List

from .Hour import Hour
from .Quarter_Hour import Quarter_Hour


class Day:
    """
    A container for 96 Quarter_Hour objects that also holds the weekday
    """



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////*   INITIALIZER   *///////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, weekday:int):
        self.weekday = weekday                                                          # save given weekday
        self.quarter_hours = [Quarter_Hour(weekday, i*15*60) for i in range(96)]        # create 96 Quarter_Hours with times corresponding to position



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////*   PRIVATE METHODS   */////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __convert_weekday(self):
        """
        Takes in an integer weekday
        Returns a string weekday
        """
        
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]       # create reference array
        return weekdays[self.weekday]                                                                   # find weekday name based on index



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////*   PUBLIC METHODS   */////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def find_free_hours(self):
        """
        Check and create an Hour object for every four in a row Quarter_Hours
        """
        
        free_hours = []                                                                 # create returnable array to fill with the Hour objects

        for index, quarter_hour in enumerate(self.quarter_hours):                       # for each Quarter_Hour object in the stored quarter hours
            if not quarter_hour.get_availability():                                     # if the first one is not free
                continue                                                                    # start over
            elif not self.quarter_hours[index + 1].get_availability():                  # or the second one is not free
                index += 1                                                                  # index past it (no point in starting the process over with this quarter when its already known to be booked)
                continue                                                                    # start over
            elif not self.quarter_hours[index + 2].get_availability():                  # or the third one is not free
                index += 2                                                                  # index past it
                continue                                                                    # start over
            elif not self.quarter_hours[index + 3].get_availability():                  # or the fourth one is not free
                index += 3                                                                  # index past it
                continue                                                                    # start over
            else:                                                                       # if all four of them are available
                free_hours.append(                                                          # create an Hour object containing all of the quarters an append it to the free hours
                    Hour([quarter_hour, 
                    self.quarter_hours[index + 1], 
                    self.quarter_hours[index + 2], 
                    self.quarter_hours[index + 3]]))

            if index >= len(self.quarter_hours):                                        # if the index goes out of bounds
                break                                                                   # stop the loop
            
        return free_hours



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////*   GETTERS   */////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def get_quarters(self):
        return self.quarter_hours



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # /////////////////////////////////////////*   TO STRING   *////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __str__(self) -> str:
        returnable_string = f"{self.__convert_weekday()}:\n"                                                                                                            # create a string with the weekday as a header
        for i, quarter in enumerate(self.quarter_hours):                                                                                                                # for every Quarter_Hour 
            quarter_str = str(quarter).replace(f"{self.__convert_weekday()} at ", "")                                                                                   # create the quarter str by chopping off the weekday from the Quarter_Hour __str__
            returnable_string = ("{}{} {}".format(returnable_string, quarter_str if len(quarter_str)>=30 else f" {quarter_str} ", '\n' if i % 4 == 3 else ''))          # add the quarter str with correct spacing and a return if needed
        returnable_string = f"{returnable_string[:-2]}\n_______________________________________________________________________________"                                # add a finishing line
        return returnable_string

    

