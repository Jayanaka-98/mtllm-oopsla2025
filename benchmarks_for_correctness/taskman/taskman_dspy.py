import dspy
from pydantic import BaseModel, Field

llm = dspy.LM('openai/gpt-4o', cache=False, )
dspy.settings.configure(lm=llm)


class Task(BaseModel):
    description: str = Field(description="Content of the Job to be done")
    time: int = Field(description="Estimated time in minutes for one to finish the job")
    priority: int = Field(description="Estimated Priority for the Task (0-10)")


class GetTask(dspy.Signature):
    """Get Task."""

    info: str = dspy.InputField(desc="Task Information")
    task: Task = dspy.OutputField()


task_contents = [
    "Have some sleep",
    "Enjoy a better weekend with my girlfriend",
    "Work on Jaseci Project",
    "Teach EECS 281 Students",
    "Enjoy family time with my parents",
]
tasks = []
for task_content in task_contents:
    task = dspy.TypedPredictor(GetTask)(info=task_content).task
    tasks.append(task)
print(tasks)
