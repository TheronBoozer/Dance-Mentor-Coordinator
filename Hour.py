

from typing import List
from Quarter_Hours import Quarter_Hours


class Hour:
    quarters = []


    def __init__(self, quarters:List[Quarter_Hours]):
        self.quarters = quarters

    def get_start_time(self):
        return self.quarters[0].get_start_time()
    
    def get_end_time(self):
        return self.quarters[-1].get_end_time()
    
    def __str__(self) -> str:
        return self.get_start_time() + " to " + self.get_end_time()