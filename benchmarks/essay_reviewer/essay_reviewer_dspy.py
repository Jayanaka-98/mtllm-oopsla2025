import dspy

llm = dspy.LM('openai/gpt-4o', cache=False, )
dspy.settings.configure(lm=llm)

class Essay:
    def __init__(self, essay: str):
        self.essay = essay

    def essay_judge(self, criteria: str) -> str:
        class EssayJudge(dspy.Signature):
            """Evaluate the given essay based on the given criteria. Provide Detailed Judgement."""

            essay: str = dspy.InputField(desc="Essay")
            criteria: str = dspy.InputField(desc="Criteria")
            judgement: str = dspy.OutputField(desc="Judgement")

        judgment = dspy.Predict(EssayJudge)(
            essay=self.essay, criteria=criteria
        ).judgement
        return judgment

    def generate_summary(self, judgements: dict) -> str:
        class GenerateSummary(dspy.Signature):
            """Generate a summary with the given judgements."""

            essay: str = dspy.InputField(desc="Essay")
            judgements: str = dspy.InputField(desc="Judgements")
            summary: str = dspy.OutputField(desc="Summary")

        summary = dspy.Predict(GenerateSummary)(
            essay=self.essay, judgements=str(judgements)
        ).summary
        return summary

    def give_grade(self, summary: str) -> str:
        class GiveGrade(dspy.Signature):
            """Give essay a letter grade (A-D)."""

            summary: str = dspy.InputField(desc="Summary")
            grade: str = dspy.OutputField(desc="Grade")

        grade = dspy.Predict(GiveGrade)(summary=summary).grade
        return grade


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
print("Reviewer Notes: ", summary)
print("Grade: ", grade)
