from typing import overload
from Scheduling.Schedule import Schedule
from Scheduling.When2Meet import When2Meet



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
        self.name = information[0]                                                      # store name
        self.email = information[1]                                                     # store email
        self.phone_number = information[2]                                              # store phone number
        self.contact_method = information[3]                                            # store the preferred contact method (email, slack, or text)

        self.schedule = Schedule().change_availability(When2Meet(information[4]))       # create and store a schedule based on their when2meet availability

        self.teaching_levels = {}                                                       # create a dictionary to store their teaching level capabilities
        self.teaching_levels["smooth"] = self.__level_conversion(information[5])        # store the smooth level
        self.teaching_levels["standard"] = self.__level_conversion(information[6])      # store standard level
        self.teaching_levels["rhythm"] = self.__level_conversion(information[7])        # store rhythm level
        self.teaching_levels["latin"] = self.__level_conversion(information[8])         # store latin level

        self.follower = information[9] == "Follower" or information[9] == "Both"        # store if they teach following steps
        self.leader = information[9] == "Leader" or information[9] == "Both"            # store if they teach leading steps



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////*   PRIVATE METHODS   */////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    @overload
    def __level_conversion(self, level:int) -> str:
        ...

    @overload
    def __level_conversion(self, level:str) -> int:
        ...

    def __level_conversion(self, level):
        """
        Converts numeric or alphabetic level information to the opposiite type
        """
        
        conversion_array = ["Unqualified", "Newcomer", "Bronze", "Silver", "Gold", "Open"]      # create reference array
        if type(level) is str:                                                                  # if the given variable is a string
            return conversion_array.index(level)                                                # return the index of said string
        elif type(level) is int:                                                                # if the given variable is an int
            return conversion_array[level]                                                      # return the string at said index
        
        

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////*   GETTERS   */////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def get_preferred_contact(self):
        """
        Return the contact information preferred by the mentor
        """
        
        match self.contact_method:              # reference their contect_method
            case "Slack":                       # if it is slack
                return self.name                # return their name
            case "Email":                       # if it is email
                return self.email               # return their email
            case "Text":                        # if it is text
                return self.phone_number        # return their phone number
            

    def get_role(self):
        """
        Returns the mentors role teaching capabilities
        """
        
        if self.follower and self.leader: return 'Leader and Follower'
        elif self.follower: return 'Follower'
        elif self.leader: return 'Leader'

    def get_schedule(self):
        return self.schedule
            


    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # /////////////////////////////////////////*   TO STRING   *////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __str__(self) -> str:
        contact = self.get_preferred_contact()
        role = self.get_role()
        return f"""
    {self.name}:
     {contact}
     {role}
     Dance Levels:
        - {self.__level_conversion(self.teaching_levels['smooth'])} in Smooth,
        - {self.__level_conversion(self.teaching_levels['standard'])} in Standard,
        - {self.__level_conversion(self.teaching_levels['rhythm'])} in Rhythm,
        - {self.__level_conversion(self.teaching_levels['latin'])} in Latin
                        """
    

        


