import dspy
from pydantic import BaseModel, Field

llm = dspy.LM('openai/gpt-4o', cache=False, )
dspy.settings.configure(lm=llm)


class Singer(BaseModel):
    """Singer."""

    name: str = Field(description="Name of the Singer")
    age: int = Field(description="Age")
    top_songs: list[str] = Field(description="His/Her's Top 2 Songs")


class GetSinger(dspy.Signature):
    """Get Person Information."""

    name: str = dspy.InputField(desc="name of the singer")
    singer: Singer = dspy.OutputField()


bruno_mars = dspy.TypedPredictor(GetSinger)(name="Bruno Mars").singer
print(
    f"{bruno_mars.name} is {bruno_mars.age} years old. His top 2 songs are {bruno_mars.top_songs}."
)
