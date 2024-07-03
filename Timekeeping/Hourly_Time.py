# imports



from typing import overload


class Hourly_Time:
    int_timestamp = 0               # the integer timestamp - an hour is 3600, a minute is 60, and a second is 1


    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////*   INITIALIZER   *///////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, timestamp):
        """
        A personalized version of the Datetime object, Hourly_Time doesn't care about dates
        Accepts integer timestamps or readable timestamps
        """
        
        if type(timestamp) == int:                                              # if the given timestamp is an integer
            self.int_timestamp = timestamp                                      # set it directly
        elif type(timestamp) == str:                                            # if its a string
            self.int_timestamp = self.__convert_time(timestamp)                 # convert the string with the helper method then set it
        else:                                                                   # otherwise
            self.int_timestamp = -1                                             # give it a time of -1



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////*   PRIVATE METHODS   */////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    @overload
    def __convert_time(self, timestamp : int) -> str:
        ...
    @overload
    def __convert_time(self, timestamp : str) -> int:
        ...

    def __convert_time(self, timestamp):
        """
        Takes in either a readable timestamp (12:00 pm) or an hourly unix timestamp (43200)
        Returns the opposite
        """
        if type(timestamp) == str:                                              # if a string is passed
            hour = int(timestamp[:timestamp.index(":")])                                # separates the hour from the string
            minute = int(timestamp[timestamp.index(":")+1:timestamp.index(" ")])        # separates the minute from the string
            is_pm = "pm" in timestamp or "PM" in timestamp                              # determines if the timestamp is in the pm

            if hour == 12 : hour = 0                                                    # fixes indexing from 12 to 0 (why the fuck does time go 12 and then 1????? like just start at 0)

            unix = hour*3600 + minute*60 + is_pm*43200                                  # final conjoining of variables to create the full time

            return unix
        
        elif type(timestamp) == int:                                            # if an integer is passed
            minute = int((timestamp % 3600) / 60)                                       # convert the minutes
            is_pm = timestamp >= 43200                                                  # determine if it is the afternoon
            hour = int((timestamp - minute*60) / 3600 - int(is_pm)*12)                  # convert the hours

            if hour == 0 : hour = 12                                                    # fix "0" hour to say 12 because american timekeeping is ass
            if minute == 0 : minute = "00"                                              # extend 0's when needed

            str_time = "{}:{} {}".format(hour, minute, "PM" if is_pm else "AM")         # put together the final string

            return str_time



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////*   GETTERS   */////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def get_int_time(self) -> int:
        return self.int_timestamp
    
    def get_str_time(self) -> str:
        return self.__convert_time(self.int_timestamp)
    


    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # /////////////////////////////////////////*   TO STRING   *////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __str__(self) -> str:
        return self.get_str_time()

    
    