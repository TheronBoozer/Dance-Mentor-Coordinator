


import json
from Scheduled_Entities.Google_Form import Google_Form


def create_session_pairings(info, form : Google_Form):

    mentor_list = info["mentor_list"]
    session_requests = info["session_requests"]

    responses = form.update_responses()

    rejected_expression = json.load(open('Saved_Information/expressions.json'))["FORM"]["SESSION_REJECTION"]

    for response in responses:
        for question in response["answers"]:
            questionId = question["questionId"]
            if not questionId == '00000000':
                sessionId = int(questionId[4:])
                mentorId = int(questionId[:4])
                answer = question["textAnswers"]["answers"][0]["value"]
                if not answer == rejected_expression:
                    session_requests[sessionId].add_mentor_option(mentor_list[mentorId], answer)

    print(responses)