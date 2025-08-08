import lmql


@lmql.query(beams=2)
def get_answer(question):
    """lmql
    import wikipedia_utils
    sample(no_repeat_ngram_size=3)
    "What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?"
    "Tho 1: I need to search Colorado orogeny, find the area that the eastern sector of the Colorado ...\n"
    "Act 2: Search 'Colorado orogeny'\n"
    "Obs 2: The Colorado orogeny was an episode of mountain building (an orogeny) ...\n"
    "Tho 3: It does not mention the eastern sector. So I need to look up eastern sector.\n"
    ...
    "Tho 4: High Plains rise in elevation from around 1,800 to 7,000 ft, so the answer is 1,800 to 7,000 ft."
    "Act 5: Finish '1,800 to 7,000 ft'"
    "{question}?\n"
    for i in range(1024):
    "[MODE] {i}:"
    if MODE == "Tho":
    "[THOUGHT] "
    elif MODE == "Act":
    " [ACTION] '[SUBJECT]\n"
    if ACTION == "Search":
    result = wikipedia_utils.search(SUBJECT[:-1]) # cutting of the consumed '
    "Obs {i}: {result}\n"
    else:
    break # action must be FINISH
    from "gpt2-xl"
    where
    MODE in ["Tho", "Act"] and stops_at(THOUGHT, "\n") and
    ACTION in ["Search", "Finish"] and len(words(THOUGHT)) > 2 and
    stops_at(SUBJECT, "'") and not "Tho" in THOUGHT
    """



question = "Where is Apple Headquaters located?"
import json
in_file = "/tmp/IN.json"
with open(in_file) as f:
    data = json.load(f)
question = data["question"]
answer = get_answer(question)
print("Question: ", question)
print("Answer: ", answer)
# question = "Who is Elon Musk?"
# answer = get_answer(question)
# print("Question: ", question)
# print("Answer: ", answer)
