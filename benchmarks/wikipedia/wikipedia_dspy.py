import dspy
import wikipedia
from dspy.predict.parameter import Parameter

llm = dspy.LM('openai/gpt-4o', cache=False, )
dspy.settings.configure(lm=llm)


class Wikipedia(Parameter):
    name = "Search"
    input_variable = "query"
    desc = "takes a search query and returns summary from wikipedia"

    def __init__(self, k=3) -> None:
        pass

    def __call__(self, query):
        return wikipedia.summary(query)


get_answer = dspy.ReAct("question -> answer", tools=[Wikipedia()])


question = "Where is Apple Headquaters located?"
result = get_answer(question=question)
print("Question: ", question)
print("Answer: ", result.answer)
question = "Who is Elon Musk?"
result = get_answer(question=question)
print("Question: ", question)
print("Answer: ", result.answer)
