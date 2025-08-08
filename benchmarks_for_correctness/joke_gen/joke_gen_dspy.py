import dspy
from dspy.teleprompt import BootstrapFewShot

llm = dspy.LM('openai/gpt-4o', cache=False, )
dspy.settings.configure(lm=llm)


examples: list[tuple[str, str]] = [
    ("How does a penguin build its house?", "Igloos it together."),
    ("Which knight invented King Arthur's Round Table?", "Sir Cumference."),
]

dataset = [
    dspy.Example(joke=example[0], punchline=example[1]).with_inputs()
    for example in examples
]


class JokeWithPunchline(dspy.Signature):
    """Tell a joke with a punchline."""

    joke: str = dspy.OutputField(desc="Joke")
    punchline: str = dspy.OutputField(desc="Punchline")


class JokeWithPunchlineModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_answer = dspy.Predict(JokeWithPunchline)

    def forward(self):
        pred = self.generate_answer()
        return dspy.Prediction(joke=pred.joke, punchline=pred.punchline)


tell_a_joke = BootstrapFewShot().compile(JokeWithPunchlineModule(), trainset=dataset)
pred = tell_a_joke()
print(f"{pred.joke}: {pred.punchline}")
