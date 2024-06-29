from Hourly_Time import Hourly_Time


class Quarter_Hours:
    available = True
    start_time = Hourly_Time(0)
    end_time = Hourly_Time(0)

    def __init__(self, start_time:int):
        self.start_time = Hourly_Time(start_time)
        self.end_time = Hourly_Time(self.start_time.get_int_time() + 15*60)



    # Getters

    def get_availability(self):
        return self.available
    
    def get_start_time(self):
        return self.start_time.__str__()
    
    def get_end_time(self):
        return self.end_time.__str__()

    # Setters

    def set_available(self):
        self.available = True

    def set_unavailable(self):
        self.available = False

    # To String

    def __str__(self) -> str:
        return "{}{} - {}\033[00m".format("\033[042m" if self.get_availability() else "\033[041m", self.get_start_time(), self.get_end_time())
