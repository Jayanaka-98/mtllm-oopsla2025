import lmql

import os

os.environ['NO_CACHE'] = '1'
class Essay:
    def __init__(self, essay: str):
        self.essay = essay

    @lmql.query(cache=False)
    def essay_judge(self, criteria: str) -> str:
        """lmql
        "Evaluate the given essay based on the given criteria. Provide Detailed Judgement.\n"
        "Essay: {self.essay}\n"
        "Criteria: {criteria}\n"
        "Judgement: [judgement]" where STOPS_AT(judgement, ".")
        return judgement
        """

    @lmql.query(cache=False)
    def generate_summary(self, judgements: dict) -> str:
        """lmql
        "Generate a summary with the given judgements.\n"
        "Essay: {self.essay}\n"
        "Judgements: {judgements}\n"
        "Summary: [summary]" where STOPS_AT(summary, ".")
        return summary
        """

    @lmql.query(cache=True)
    def give_grade(self, summary: str) -> str:
        """lmql
        "Give essay a letter grade (A-D).\n"
        "Summary: {summary}\n"
        "Grade: [grade]" where STOPS_AT(grade, ".")
        return grade
        """


essay = """With a population of approximately 45 million Spaniards and 3.5 million immigrants,
        Spain is a country of contrasts where the richness of its culture blends it up with
        the variety of languages and dialects used. Being one of the largest economies worldwide,
        and the second largest country in Europe, Spain is a very appealing destination for tourists
        as well as for immigrants from around the globe. Almost all Spaniards are used to speaking at
        least two different languages, but protecting and preserving that right has not been
        easy for them.Spaniards have had to struggle with war, ignorance, criticism and the governments,
        in order to preserve and defend what identifies them, and deal with the consequences."""

essay = Essay(essay)
criterias = ["Clarity", "Originality", "Evidence"]
judgements = {}
for criteria in criterias:
    judgement = essay.essay_judge(criteria)
    judgements[criteria] = judgement
summary = essay.generate_summary(judgements)
grade = essay.give_grade(summary)
print(summary)
print(grade)
