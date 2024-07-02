import requests
from Scheduling.Schedule import Schedule


class Mentor:
    schedule = Schedule()
    name = ""
    email = ""
    phone_number = ""
    contact_method = ""
    follower = False
    leader = False
    teaching_levels = {
        "smooth" : 0,
        "standard" : 0,
        "rhythm" : 0,
        "latin" : 0
    }

    
    def __init__(self, information):
        self.name = information[0]
        self.email = information[1]
        self.phone_number = information[2]
        self.contact_method = information[3]
        # when2meet schedule conversion          TODO
        self.teaching_levels["smooth"] = self.level_conversion(information[5])
        self.teaching_levels["standard"] = self.level_conversion(information[6])
        self.teaching_levels["rhythm"] = self.level_conversion(information[7])
        self.teaching_levels["latin"] = self.level_conversion(information[8])
        self.follower = information[9] == "Follower" or information[9] == "Both"
        self.leader = information[9] == "Leader" or information[9] == "Both"



    def level_conversion(self, level):
        conversion_array = ["Unqualified", "Newcomer", "Bronze", "Silver", "Gold", "Open"]
        if type(level) is str:
            return conversion_array.index(level)
        elif type(level) is int:
            return conversion_array[level]
        
        
    def get_preferred_contact(self):
        match self.contact_method:
            case "Slack":
                return self.name
            case "Email":
                return self.email
            case "Text":
                return self.phone_number
            

    def get_role(self):
        if self.follower and self.leader: return 'Leader and Follower'
        elif self.follower: return 'Follower'
        elif self.leader: return 'Leader'
            
        
    def __str__(self) -> str:
        contact = self.get_preferred_contact()
        role = self.get_role()
        return "{}:\n    {},\n    {},\n    Dance Levels:\n    - {} in Smooth,\n    - {} in Standard,\n    - {} in Rhythm,\n    - {} in Latin".format(self.name, contact, role, self.level_conversion(self.teaching_levels['smooth']), self.level_conversion(self.teaching_levels['standard']), self.level_conversion(self.teaching_levels['rhythm']), self.level_conversion(self.teaching_levels['latin']))
    

        


def get_mentors(mentor_sheet_link:str):   
    
    csv_link = mentor_sheet_link[:mentor_sheet_link.index('edit')] + 'export?format=csv' #Converts basic 'share' link to a readable csv link

    mentor_sheet = requests.get(csv_link)
    unorganized_data = mentor_sheet.text
    row_data = unorganized_data.split('\r')

    mentor_information = []
    for row in row_data:
        mentor = row.split(',')
        mentor.pop(0)
        mentor_information.append(mentor)

    mentor_information.pop(0)

    # print(mentor_information)

    mentors = []
    for mentor in mentor_information:
        # print(mentor)
        mentors.append(Mentor(mentor))

    return mentors
                