import math

class Schedule:

    calendar_bookings = [
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False]
    ]
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
        "Time" : {
            "09" : 0,
            "10" : 1,
            "11" : 2,
            "12" : 3,
            "13" : 4,
            "14" : 5,
            "15" : 6,
            "16" : 7,
            "17" : 8,
            "18" : 9,
            "19" : 10,
            "20" : 11,
            "21" : 12,
            "22" : 13
        }
    }



   
    
    def __init__(self, start_end_times, monday_date):
        self.monday_date = monday_date
        self.times_to_cal(start_end_times)

    def __init__(self):
        self.monday_date = 0
        self.calendar_bookings = self.calendar_bookings
    

    def set_calendar_bookings(self, calendar):
        self.calendar_bookings = calendar
        
    def reset_calendar_bookings(self):
        self.calendar_bookings = [
            [False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False]
        ]
        return self.calendar_bookings