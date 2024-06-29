from typing import List

from Hour import Hour
from Quarter_Hours import Quarter_Hours


class Day:
    quarter_hours = [Quarter_Hours(i*15*60) for i in range(96)]
    free_hours = []
    weekday = ""


    def __init__(self, weekday:str):
        self.weekday = weekday

    def __init__(self, weekday:int):
        weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.weekday = weekdays[weekday]


    def get_free_hours(self):
        for index, quarter_hour in enumerate(self.quarter_hours):
            if not quarter_hour.get_availability():
                continue
            elif not Quarter_Hours[index + 1].get_availability():
                index += 1
                continue
            elif not Quarter_Hours[index + 2].get_availability():
                index += 2
                continue
            elif not Quarter_Hours[index + 3].get_availability():
                index += 3
                continue
            else:
                self.free_hours.append(Hour([quarter_hour, Quarter_Hours[index + 1], Quarter_Hours[index + 2], Quarter_Hours[index + 3]]))



    def set_divisions(self, divisions:List[Quarter_Hours]):
        self.quarter_hours = divisions


    def __str__(self) -> str:
        returnable_string = f"{self.weekday}:\n"
        for i, quarter in enumerate(self.quarter_hours):
            returnable_string = ("{}{} {}".format(returnable_string, quarter.__str__() if len(quarter.__str__())>=30 else f" {quarter.__str__()} ", '\n' if i % 4 == 3 else ''))
        returnable_string = f"{returnable_string[:-2]}\n_______________________________________________________________________________"
        return returnable_string

    

