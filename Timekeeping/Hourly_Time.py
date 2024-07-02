class Hourly_Time:
    int_timestamp = 0


    # Initializers
    def __init__(self, int_timestamp:int):
        self.int_timestamp = int_timestamp

    @classmethod
    def from_string(self, readable_timestamp:str):
        return Hourly_Time(self.__convert_time(readable_timestamp))

    # Getters
    def get_int_time(self) -> int:
        return self.int_timestamp
    
    def get_str_time(self) -> str:
        return self.__convert_time(self.int_timestamp)
    

    # To String
    def __str__(self) -> str:
        return self.get_str_time()


# Helping Functions for converting the time
    def __convert_time(self, timestamp : str) -> int :
        """Takes in either the readable timestamp (12:00 pm) and converts it to an hourly unix timestamp (43200) or vice versa"""
        hour = int(timestamp[:timestamp.index(":")])
        minute = int(timestamp[timestamp.index(":"):timestamp.index(" ")])
        is_pm = timestamp.contains("pm") or timestamp.contains("PM")

        if hour == 12 : hour = 0

        unix = hour*3600 + minute*60 + is_pm*43200

        return unix



    def __convert_time(self, timestamp : int) -> str :
        """Takes in either the readable timestamp (12:00 pm) and converts it to an hourly unix timestamp (43200) or vice versa"""
        minute = int((timestamp % 3600) / 60)
        is_pm = timestamp >= 43200
        hour = int((timestamp - minute*60) / 3600 - int(is_pm)*12)

        if hour == 0 : hour = 12
        if minute == 0 : minute = "00"

        str_time = "{}:{} {}".format(hour, minute, "PM" if is_pm else "AM")

        return str_time
    
    