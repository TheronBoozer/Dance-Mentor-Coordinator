import datetime
import math

from Day import Day

class Schedule:

    calendar_vacancies = [Day(i) for i in range(7)] * 7

    def __init__(self):
        self.calendar_vacancies = self.reset_calendar_vacancies()

        
    def reset_calendar_vacancies(self):
        self.calendar_vacancies = [Day(i) for i in range(7)] * 7
        return self.calendar_vacancies
    

    # def set_calendar_vacancies(self, unix_times, open_time, close_time):
        
        
    #     start_end_positions = [[0, open_time, close_time],]*7
        

    #     for unix in unix_times:
    #         date_time = datetime.datetime.fromtimestamp(unix)

    #         day_position = int(date_time.strftime("%w"))
    #         # print(day_position)

    #         hour = date_time.strftime("%H")
    #         # print(hour)
    #         minute = date_time.strftime("%M") 
    #         # print(minute)
    #         time_position = math.ceil((int(hour) + int(minute)/60) * 4)
    #         # print(time_position)

    #         start_end_positions[day_position].insert(-1, time_position)


    #     # print(start_end_positions)

    #     calendar = self.calendar_vacancies
    #     vacant = True
    #     for day_count, day in enumerate(calendar):
    #         for time_count, time in enumerate(day):
    #             if time_count in start_end_positions[day_count]:
    #                 vacant = not vacant


    #             calendar[day_count][time_count] = vacant
    #         vacant = True

    #     # print(calendar[4])

    #     self.calendar_vacancies = calendar



    # # def is_available(self, day, start_time, end_time):
    # #     for time in self.calendar_vacancies[day]:
    # #         if not time:
    # #             return False
            
    # #     return True