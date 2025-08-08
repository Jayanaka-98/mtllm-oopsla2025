import lmql
from dataclasses import dataclass


@dataclass
class Person:
    full_name: str
    yod: int
    personality: str


@lmql.query()
def personality_finder(name: str) -> Person:
    """lmql
    "Personality should be Introvert or Extrovert or Ambivert\n"
    "Get the Person object for {name}.\n"
    "Structured: [PERSON_DATA]\n" where type(PERSON_DATA) is Person
    return PERSON_DATA
    """

import json
in_file = "/tmp/IN.json"
with open(in_file) as f:
    data = json.load(f)
name = data["name"]
person = personality_finder(name)
print(
    f"{person.full_name} was an {person.personality} person who died in {person.yod}."
)
