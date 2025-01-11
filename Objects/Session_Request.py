import re

from Objects.Scheduling.When2Meet import When2Meet
from Objects.Scheduling.Schedule import Schedule

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

        self.styles = information[7].split(", ")                                        # save the styles covered
        self.parts = information[6].split(", ")                                         # save the parts covered
        self.topic = (                                                                  # create the topic
        f"""{information[5]} {information[4]} -
        Roles: {information[6].replace('ing', 'er')}
        Styles: {information[7]}
        Dances: {information[8]}""")

        self.description = information[9]                                               # save the provided description
        self.mentor_preference = information[10].split(", ")                            # create the array of mentor names
        self.assigned_mentor = [0, None, "No available time"]                           # create an array to save the highest rated mentor
        self.assistant_mentor = information[11].strip() == 'Yes'                        # save a boolean as to if an assistant is welcome
        

    
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
    # ///////////////////////////////////////*   PUBLIC METHODS   */////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def add_mentor_option(self, mentor_answers):

        match_rating = mentor_answers[0]
        mentor = mentor_answers[1]
        time = mentor_answers[2]

        if mentor.get_name() in self.mentor_preference:
            match_rating += 100 + self.mentor_preference.index(mentor.get_name())

        qualifiers = mentor.get_teaching_levels()

        for style in self.styles:
            match_rating += qualifiers[style]["Level"]

            for part in self.parts:
                match_rating += int(part in qualifiers[style]["Part"])

        if match_rating > self.assigned_mentor[0]:
            self.assigned_mentor = [match_rating, mentor, time]


    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////*   GETTERS   */////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////

    def get_schedule(self) -> Schedule:
        return self.schedule
    
    def get_participants(self) -> str:
        return self.participants
    
    def get_topic(self) -> str:
        return self.topic
    
    def get_description(self) -> str:
        return self.description
    
    def get_mentor(self) -> list:
        return self.assigned_mentor
    
    def get_emails(self) -> list:
        return self.emails
    
    def get_numbers(self) -> str:
        return self.phone_numbers
    

    
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