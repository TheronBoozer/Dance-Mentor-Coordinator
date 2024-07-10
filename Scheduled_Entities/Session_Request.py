import re

from Scheduling.When2Meet import When2Meet
from Scheduling.Schedule import Schedule

class Session_Request:
    """
    An object to hold detailing of session requests including a schedule
    """



    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////*   INITIALIZER   *///////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __init__(self, information):
        self.participants = information[0]                                              # save the names of the participants
        self.schedule = Schedule()                                                      # create a schedule

        self.emails = self.__parse_emails(information[1])                               # save a list of emails
        self.phone_numbers = self.__parse_phone_numbers(information[2])                 # save a list of phone numbers

        self.when2meet_link = information[3]                                            # save the when2meet link
        self.when2meet = When2Meet(self.when2meet_link)                                 # create the when2meet object
        self.schedule.change_availability(self.when2meet)                               # update the schedule based on the when2meet

        self.level = information[5]                                                     # save the level
        self.topic = f"{information[4]} - {information[6]} : {information[7]}"          # create the topic ex: (Technique - Smooth, Standard : Tango, Waltz)
        self.description = information[8]                                               # save the provided description
        self.mentor_preference = information[9].split(", ")                             # create the array of mentor names
        self.assistant_mentor = information[10].strip() == 'Yes'                        # save a boolean as to if an assistant is welcome
        


    
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////*   PRIVATE_METHODS   */////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __parse_emails(self, email_string : str):
        """
        Given a string of emails, parse and return an array of the emails
        """
        
        emails = re.findall(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", email_string)              # regex!!

        return emails

    def __parse_phone_numbers(self, phone_string : str):
        """
        Given a string of phone numbers, parse and return an array of the numbers
        """
        
        numbers = re.findall(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", phone_string)          # more regex!!

        return numbers

    

    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////*   GETTERS   */////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def get_schedule(self) -> Schedule:
        return self.schedule
    

    
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # /////////////////////////////////////////*   TO STRING   *////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def __str__(self) -> str:
        return f"""
    {self.participants}:
     emails - {", ".join(self.emails)}
     phone numbers - {", ".join(self.phone_numbers)}
     availability - {self.when2meet_link}
     session details:
        level: {self.level}
        topic: {self.topic}
        description: {self.description}
     mentor preferences:
        main mentor options - {", ".join(self.mentor_preference)}
        assistant mentor - {self.assistant_mentor}
                """