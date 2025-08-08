import lmql


@lmql.query()
def odd_word_out(question: str, choices: str):
    '''lmql
    """Q: {question}\n
    Answer Choices: {choices}
    """
    "A: Let's think step by step.\n"
    "[REASONING]"
    # constrain the final answer to robustly extract the result
    "Therefore, among A through F, the answer is[RESULT]" where \
    RESULT in ["A", "B", "C", "D", "E", "F"]

    # return just the RESULT to the caller
    return REASONING,RESULT 
    '''

import json
in_file = "/tmp/IN.json"

with open(in_file) as f:
    data = json.load(f)
question = data["question"]
choices = data["choices"]
print("\n".join(odd_word_out(question, choices)))
