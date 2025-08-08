import lmql
import os

os.environ['NO_CACHE'] = '1'


@lmql.query(cache=False)
def tell_a_joke():
    '''lmql
    """A list good dad joke. A indicates the punchline:
    Q: How does a penguin build its house?
    A: Igloos it together.
    Q: Which knight invented King Arthur's Round Table?
    A: Sir Cumference.
    Q:[JOKE]
    A:[PUNCHLINE]"""  where len(TOKENS(JOKE)) < 120 and  STOPS_AT(JOKE, "?") and  STOPS_AT(PUNCHLINE, "\n") and  len(TOKENS(PUNCHLINE)) > 1
    return f'{JOKE} : {PUNCHLINE}'
    '''


print(tell_a_joke())
