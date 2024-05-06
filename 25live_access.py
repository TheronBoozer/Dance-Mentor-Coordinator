import requests
import json
from bs4 import BeautifulSoup



def main():
    print("calendar:")
    response = requests.get("https://25live.collegenet.com/25live/data/wpi/run/rm_reservations.ics?caller=pro&space_id=353&start_dt=0&end_dt=+7&options=standard")
    soup = BeautifulSoup(response.text, "html.parser")
    soup.prettify

    cal_text = soup.text
    cal_data = cal_text.split("\n")

    cal_times = []
    for data in cal_data:
        if data.startswith("DTSTART;TZID=America/New_York:"):
            dt = data.removeprefix("DTSTART;TZID=America/New_York:")

        elif data.startswith("DTEND;TZID=America/New_York:"):
            dt = data.removeprefix("DTEND;TZID=America/New_York:")

        else:
            continue
        
        dt = dt[4:15]
        cal_times.append(dt)

    
    print(cal_times)


main()
