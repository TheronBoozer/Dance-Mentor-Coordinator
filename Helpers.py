import datetime
import time

# ----- convert 25Live timestamp to unix timestamp -----
def timestamp_to_unix(timestamp : str) -> int :
    """Takes in the 25Live timestamp (`"20240225T070438/r"`) and converts it to unix timestamp (`1708862678`)"""
    return int(time.mktime(datetime.datetime.strptime(str(timestamp[:-1:]), "%Y%m%dT%H%M%S").timetuple()))