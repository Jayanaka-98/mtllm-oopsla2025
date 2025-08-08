import lmql


@lmql.query()
def translate(english_word):
    '''lmql
    """
        "sea otter": "loutre de mer",
        "peppermint": "menthe poivrée",
        "plush giraffe": "girafe en peluche"
    """
    "Q: What is the translation of {english_word}?\n"
    "A:[ANSWER]"
    return f'{ANSWER}'
    '''

import json
in_file = "/tmp/IN.json"
with open(in_file) as f:
    data = json.load(f)
english_word = data["english_word"]
print(translate(english_word))
