import lmql
from dataclasses import dataclass


@dataclass
class Songs:
    song1: str
    song2: str


@dataclass
class Singer:
    name: str
    age: int
    top_2_songs: Songs


@lmql.query
def get_singer(name):
    """lmql
    "name: {name}.\n"
    "Structured: [PERSON_DATA]\n" where type(PERSON_DATA) is Singer
    return PERSON_DATA
    """


bruno_mars = get_singer("Bruno Mars")
print(
    f"{bruno_mars.name} is {bruno_mars.age} years old. His top 2 songs are {bruno_mars.top_2_songs.song1} & {bruno_mars.top_2_songs.song2}."
)
