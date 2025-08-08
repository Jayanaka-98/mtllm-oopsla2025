import lmql


@lmql.query
def odd_word_out(OPTIONS):
    """lmql
   
    "Pick the odd word out: skirt, dress, pen, jacket.\n"
    "skirt is clothing, dress is clothing, pen is an object, jacket is clothing.\n"
    "So the odd one is pen.\n\n"
    "Pick the odd word out: Spain, France, German, England, Singapore.\n"
    "Spain is a country, France is a country, German is a language, ...\n"
    "So the odd one is German.\n\n"
    "Pick the odd word out: {OPTIONS}\n"
    "[REASONING]"
    "[RESULT]" 
    # where \
    #     not "\n" in REASONING and not "Pick" in REASONING
    return REASONING,RESULT 
    """

import json
in_file = "/tmp/IN.json"
with open(in_file) as f:
    data = json.load(f)
OPTIONS = data["options"]
print(odd_word_out(OPTIONS))
