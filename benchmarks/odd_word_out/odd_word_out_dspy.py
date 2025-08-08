import dspy
# from dspy.teleprompt import BootstrapFewShot

llm = dspy.LM('openai/gpt-4o', cache=False, )
dspy.settings.configure(lm=llm)

# examples: list[tuple[list, str, str]] = [
#     (
#         ["skirt", "dress", "pen", "jacket"],
#         "skirt is clothing, dress is clothing, pen is an object, jacket is clothing.",
#         "pen",
#     ),
#     (
#         ["Spain", "France", "German", "England", "Singapore"],
#         "Spain, France, England, Singapore is a country, German is a language.",
#         "German",
#     ),
# ]

# dataset = [
#     dspy.Example(
#         options=str(example[0]), reasoning=example[1], odd_word=example[2]
#     ).with_inputs("options")
#     for example in examples
# ]


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
pred = get_odd_word_out("[Bentley, Ferrari, Lamborghini, Casio, Toyota]")
print((pred.rationale, pred.odd_word))
