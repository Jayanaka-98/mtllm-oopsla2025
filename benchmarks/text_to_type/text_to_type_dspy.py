import dspy
from pydantic import BaseModel, Field

llm = dspy.LM('openai/gpt-4o', cache=False, )
dspy.settings.configure(lm=llm)


class Employer(BaseModel):
    employer_name: str = Field(description="Employer Name")
    location: str = Field(description="Location")


class Person(BaseModel):
    name: str = Field(description="Name")
    age: int = Field(description="Age")
    job: str = Field(description="Job")
    employer: Employer = Field(description="Employer")


class GetPerson(dspy.Signature):
    """Get Person Information."""

    info: str = dspy.InputField(desc="Person Information")
    person: Person = dspy.OutputField()


info = "Alice is a 21 years old and works as an engineer at LMQL Inc in Zurich, Switzerland."
alice = dspy.TypedPredictor(GetPerson)(info=info).person
print(f"Their name is {alice.name} and she works in {alice.employer.location}.")
