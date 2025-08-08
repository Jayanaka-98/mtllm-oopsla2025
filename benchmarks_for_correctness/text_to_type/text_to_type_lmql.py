import lmql
from dataclasses import dataclass


@dataclass
class Employer:
    employer_name: str
    location: str


@dataclass
class Person:
    name: str
    age: int
    employer: Employer
    job: str


@lmql.query
def person_data(info):
    """lmql
    "{info}\n"
    "Structured: [PERSON_DATA]\n" where type(PERSON_DATA) is Person
    return PERSON_DATA
    """
import json
in_file = "/tmp/IN.json"
with open(in_file) as f:
    data = json.load(f)
info = data["info"]
alice = person_data(info)
print(alice)
print(f"Their name is {alice.name} and she works in {alice.employer.location}.")
