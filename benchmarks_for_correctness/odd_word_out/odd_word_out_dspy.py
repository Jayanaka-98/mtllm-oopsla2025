import dspy
# from dspy.teleprompt import BootstrapFewShot

llm = dspy.LM('openai/gpt-4o', cache=False, )
dspy.settings.configure(lm=llm)

class OddWordOut(dspy.Signature):
    """Pick the Odd Word Out from the given list of words."""

    options: str = dspy.InputField(desc="Options to pick from")
    odd_word: str = dspy.OutputField(desc="Odd Word")


class OddWordOutModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_answer = dspy.ChainOfThought(OddWordOut)

    def forward(self, options: str):
        prediction = self.generate_answer(options=options)
        print(prediction)
        return dspy.Prediction(
            odd_word=prediction.odd_word, rationale=prediction.reasoning
        )


get_odd_word_out = OddWordOutModule()
options = "[Bentley, Ferrari, Lamborghini, Casio, Toyota]"
import json
in_file = "/tmp/IN.json"
with open(in_file) as f:
    data = json.load(f)
options = data["options"]
pred = get_odd_word_out(options)
print((pred.rationale, pred.odd_word))
