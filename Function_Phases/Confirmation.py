


import json
from Scheduled_Entities.Google_Form import Google_Form


def create_session_pairings(info, form : Google_Form):

    mentor_list = info["mentor_list"]
    session_requests = info["session_requests"]

    responses = form.update_responses()

    rejected_expression = json.load(open('Saved_Information/expressions.json'))["FORM"]["SESSION_REJECTION"]

    for response in responses:
        for question in response["answers"].values():
            
            question_id = question["questionId"]

            if question_id == "00000000" or 'b' in question_id:
                continue

            session_id = question_id[5:]
            mentor_id = question_id[:4]
            linked_question = response["answers"][question_id.replace('a', 'b')]

            answer = question["textAnswers"]["answers"][0]["value"]
            
            match_rating = int(linked_question["textAnswers"]["answers"][0]["value"]) * 10

            if not answer == rejected_expression:
                session_requests[int(session_id) - 1].add_mentor_option([match_rating, mentor_list[int(mentor_id) - 1], answer])




    for session in session_requests:
        print(session.get_mentor())