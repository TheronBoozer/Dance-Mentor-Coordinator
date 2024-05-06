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
    

    def times_to_cal(start_end_times):
        for dt in start_end_times:
            t_string = dt[dt.index("t")+1]
            t_int = int(t_string)
            time = math.ceil(t_int / 10000)
            print(time)
        
