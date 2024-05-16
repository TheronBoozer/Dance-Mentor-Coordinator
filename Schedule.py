import math

class Schedule:

    calendar_bookings = [[]]
    monday_date = ""

    conversion_dict = {
        "Day" : {
            "Monday" : 0,
            "Tuesday" : 1,
            "Wednesday" : 2,
            "Thursday" : 3,
            "Friday" : 4,
            "Saturday" : 5,
            "Sunday" : 6
        }, 
    }



   
    
    def __init__(self, start_end_times, monday_date):
        self.monday_date = monday_date
        self.times_to_cal(start_end_times)

    def __init__(self):
        self.calendar_bookings = self.reset_calendar_bookings()
    


    def set_calendar_bookings(self, calendar):
        self.calendar_bookings = calendar
        
    def reset_calendar_bookings(self):
        self.calendar_bookings = [
            [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        ]
        return self.calendar_bookings