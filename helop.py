import datetime
import time

# ----- convert ce timestamp to unix timestamp -----
def timestamp_to_unix(timestamp : str) -> int :
    """Takes in the CE timestamp (`"2024-02-25T07:04:38.000Z"`) and converts it to unix timestamp (`1708862678`)"""
    return int(time.mktime(datetime.datetime.strptime(str(timestamp[:-5:]), "%Y-%m-%dT%H:%M:%S").timetuple()))