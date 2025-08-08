import lmql

from dataclasses import dataclass


@dataclass
class Task:
    description: str
    time: int
    priority: int


@lmql.query
def GetTask(info: str) -> Task:
    """lmql
    "Enjoy a better weekend with my girlfriend.\n"
    "Structured: [TASK_DATA]\n" where type(TASK_DATA) is Task
    return TASK_DATA
    """


task_contents = [
    "Have some sleep",
    "Enjoy a better weekend with my girlfriend",
    "Work on Jaseci Project",
    "Teach EECS 281 Students",
    "Enjoy family time with my parents",
]
tasks = []
for task_content in task_contents:
    task = GetTask(task_content)
    tasks.append(task)

print(tasks)

"""
[Task(description='Enjoy a better weekend with my girlfriend.', time=2, priority=1), 
Task(description='Enjoy a better weekend with my girlfriend.', time=2, priority=1), 
Task(description='Enjoy a better weekend with my girlfriend.', time=21, priority=21), 
Task(description='Enjoy a better weekend with my girlfriend.', time=2, priority=1),
 Task(description='Enjoy a better weekend with my girlfriend.', time=2, priority=1)]
 """
