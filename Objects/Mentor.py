from typing import overload
from Objects.Scheduling.Schedule import Schedule
from Objects.Scheduling.When2Meet import When2Meet



class Mentor:
    """
    Creates a dance mentor and stores their preferences and levels
    """

    

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////*   INITIALIZER   *///////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, information):
        self.name = information[0]                                                                  # store name
        self.email = information[1]                                                                 # store email
        self.phone_number = information[2]                                                          # store phone number
        self.schedule = Schedule().change_availability(When2Meet(information[4]))                   # create and store a schedule based on their when2meet availability

        

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////*   GETTERS   */////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
            
    
    def get_email(self):
        return self.email

    def get_schedule(self):
        return self.schedule
    
    def get_name(self):
        return self.name
    
    def get_phone_number(self):
        return self.phone_number
            


    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # /////////////////////////////////////////*   TO STRING   *////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __str__(self) -> str:
        return f"""
    {self.name}:
        {self.email}
        {self.phone_number}"""
    

        


