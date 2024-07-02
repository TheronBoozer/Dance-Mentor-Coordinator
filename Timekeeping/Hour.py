from typing import List
from Timekeeping.Quarter_Hour import Quarter_Hour


class Hour:
    quarters = []


    def __init__(self, quarters:List[Quarter_Hour]):
        self.quarters = quarters

    def get_start_time(self):
        return self.quarters[0].get_start_time()
    
    def get_end_time(self):
        return self.quarters[-1].get_end_time()
    
    def __str__(self) -> str:
        return self.get_start_time() + " to " + self.get_end_time()