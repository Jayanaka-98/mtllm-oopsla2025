import dspy
from dspy.teleprompt import BootstrapFewShot

llm = dspy.LM('openai/gpt-4o', cache=False, )
dspy.settings.configure(lm=llm)

examples: dict[str, str] = {
    "sea otter": "loutre de mer",
    "peppermint": "menthe poivrée",
    "plush giraffe": "girafe en peluche",
}

dataset = [
    dspy.Example(english_word=english_word, translation=translation).with_inputs(
        "english_word"
    )
    for english_word, translation in examples.items()
]


class Translation(dspy.Signature):
    """Translate the given English word"""

    english_word: str = dspy.InputField(desc="English word to translate")
    translation: str = dspy.OutputField(desc="Translation")


class TranslationModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_answer = dspy.Predict(Translation)

    def forward(self, english_word: str):
        prediction = self.generate_answer(english_word=english_word)
        return dspy.Prediction(translation=prediction.translation)


translate = BootstrapFewShot().compile(TranslationModule(), trainset=dataset)
pred = translate(english_word="cheese")
print(pred.translation)
