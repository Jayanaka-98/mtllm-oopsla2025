import dspy

dspy.settings.cache = None

llm = dspy.LM('openai/gpt-4o', temperature=0.2, cache=False, )
dspy.settings.configure(lm=llm)

# dspy.configure_cache(
#     enable_disk_cache=False,
#     enable_memory_cache=False,
# )

class GetExpert(dspy.Signature):
    """Find the Expert Profession to answer the given question."""

    question: str = dspy.InputField()
    expert: str = dspy.OutputField(desc="Expert Profession")


class GetAnswer(dspy.Signature):
    """Get the Expert's answer to the given question."""

    question: str = dspy.InputField()
    expert: str = dspy.InputField()
    answer: str = dspy.OutputField(desc="Expert's answer")


question = "What are Large Language Models?"
expert = dspy.Predict(GetExpert)(question=question).expert
answer = dspy.Predict(GetAnswer)(question=question, expert=expert).answer
print(f"{expert} says: {answer}")
