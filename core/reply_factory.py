
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)
    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if not current_question_id:
        return True, ""
    
    ans = 0
    try: 
        ans = int(answer)
        if ans<0 or ans>4:
            raise ValueError("Number range")
    except:
        print("wrong format")
        return False, "Please input Number between 1 and 4"

    ans_list = session.get('ans_list', [])

    if(len(ans_list)==0):
        ques_nos = len(PYTHON_QUESTION_LIST)
        session['ans_list'] = [-1 for x in range(ques_nos+1)]
        ans_list = session['ans_list']
    
    ans_list[current_question_id-2] = ans
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if not current_question_id:
        current_question_id=1

    ques_nos = len(PYTHON_QUESTION_LIST)
    if current_question_id>ques_nos:
        return False, -1

    ques = (f"Qn {str(current_question_id)} : ")
    ques += PYTHON_QUESTION_LIST[current_question_id-1]["question_text"]
    ques += "\n"
    i=1
    for op in PYTHON_QUESTION_LIST[current_question_id-1]["options"]:
        ques += (f"\n Option {str(i)} => {op}")
        i += 1

    return ques, current_question_id+1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    ans_list = session['ans_list']
    no_of_question = len(PYTHON_QUESTION_LIST)
    correct_ans = []
    final_result = "Thank you for taking quiz. \nHere is your result: \n"

    for x in PYTHON_QUESTION_LIST:
        option = x["options"]
        ans = x["answer"]
        try:
            index = option.index(ans)
            correct_ans.append(index+1)
        except ValueError:
            correct_ans.append(ans)

    i=0
    correct_ans_nos = 0

    while(i<no_of_question):
        final_result += (f" Qn. {i+1}: Ans: {correct_ans[i]}, \t Your Ans {ans_list[i]} \n")
        
        if correct_ans[i]==ans_list[i]:
            correct_ans_nos+=1
        i += 1

    final_result+=(f"\nTotal: {no_of_question}, Correct: {correct_ans_nos} ({100*correct_ans_nos/no_of_question})%")
    final_result+="\nEnter any key to try again!"


    return final_result
