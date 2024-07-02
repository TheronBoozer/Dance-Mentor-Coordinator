import requests
from Scheduling.Schedule import Schedule
from Scheduling.Twenty_Five_Live_Calendar import Twenty_Five_Live_Calendar
from Scheduling.When2Meet import When2Meet




class Location:
    schedule = Schedule()
    name = ""
    when2meet_link = ""
    twenty_five_live_link = ""

    # Initializer
    def __init__(self, information):
        self.name = information[0]
        self.twenty_five_live_link = information[1]
        self.when2meet_link = information[2]
        self.__update()

    # Private Methods



def get_locations(location_sheet_link):
    csv_link = location_sheet_link[:location_sheet_link.index('edit')] + 'export?format=csv' #Converts basic 'share' link to a readable csv link

    location_sheet = requests.get(csv_link)
    unorganized_data = location_sheet.text
    row_data = unorganized_data.split('\r')

    location_information = []
    for row in row_data:
        location = row.split(',')
        location.pop(0)
        location_information.append(location)

    location_information.pop(0)

    locations = []
    for location in location_information:
        # print(mentor)
        location.append(Location(location))

    return locations


