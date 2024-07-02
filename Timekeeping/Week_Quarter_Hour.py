

from Timekeeping.Quarter_Hour import Quarter_Hour


class Week_Quarter_Hour():
    quarter_hour = Quarter_Hour(0)
    weekday = 0

    def __init__(self, weekday:int, quarter_hour:Quarter_Hour):
        self.weekday = weekday
        self.quarter_hour = quarter_hour

    @classmethod
    def from_int(self, weekday, quarter_int:int):
        quarter_hour = Quarter_Hour(quarter_int)
        return Week_Quarter_Hour(weekday, quarter_hour)


    # private methods
    def __convert_weekday(self):
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return weekdays[self.weekday]

    # getters
    def get_weekday(self):
        return self.weekday
    
    def get_quarter_hour(self):
        return self.quarter_hour
    
    # to string
    def __str__(self) -> str:
        return f"{self.__convert_weekday()} at {str(self.quarter_hour)}"