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
        self.name = information[0]                                                                  # store name
        self.email = information[1]                                                                 # store email
        self.phone_number = information[2]                                                          # store phone number
        self.contact_method = information[3]                                                        # store the preferred contact method (email, slack, or text)

        self.schedule = Schedule().change_availability(When2Meet(information[4]))                   # create and store a schedule based on their when2meet availability

        self.teaching_levels = {                                                                    # create a dictionary to store their teaching level capabilities
            "Smooth" : {},
            "Standard" : {},
            "Rhythm" : {},
            "Latin" : {}
        }

        self.teaching_levels["Smooth"]["Level"] = self.__level_conversion(information[5])           # store the smooth level as an int
        self.teaching_levels["Standard"]["Level"] = self.__level_conversion(information[6])         # store standard level as an int
        self.teaching_levels["Rhythm"]["Level"] = self.__level_conversion(information[7])           # store rhythm level as an int
        self.teaching_levels["Latin"]["Level"] = self.__level_conversion(information[8])            # store latin level as an int

        self.teaching_levels["Smooth"]["Part"] = self.__part_conversion(information[9])             # store the smooth part as str
        self.teaching_levels["Standard"]["Part"] = self.__part_conversion(information[10])          # store standard part as str
        self.teaching_levels["Rhythm"]["Part"] = self.__part_conversion(information[11])            # store rhythm part as str
        self.teaching_levels["Latin"]["Part"] = self.__part_conversion(information[12])             # store latin part as str



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
        

    def __part_conversion(self, part : str) -> str:

        return str(part).split(', ')

        

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
            
    
    def get_email(self):
        return self.email
            

    # def get_role(self):
    #     """
    #     Returns the mentors role teaching capabilities
    #     """
        
    #     if self.follower and self.leader: return 'Leader and Follower'
    #     elif self.follower: return 'Follower'
    #     elif self.leader: return 'Leader'

    def get_schedule(self):
        return self.schedule
    
    def get_name(self):
        return self.name
    
    def get_teaching_levels(self):
        return self.teaching_levels
    
    def get_phone_number(self):
        return self.phone_number
            


    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # /////////////////////////////////////////*   TO STRING   *////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __str__(self) -> str:
        contact = self.get_preferred_contact()
        return f"""
    {self.name}:
     {contact}
     Dance Levels:
        - {self.__level_conversion(self.teaching_levels['Smooth'])} in Smooth,
        - {self.__level_conversion(self.teaching_levels['Standard'])} in Standard,
        - {self.__level_conversion(self.teaching_levels['Rhythm'])} in Rhythm,
        - {self.__level_conversion(self.teaching_levels['Latin'])} in Latin
                        """
    

        


