import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o");

obj Task {
    has description: str, time_in_min: int, priority_out_of_10: int;
}

with entry {
    task_contents = [
        "Have some sleep", "Enjoy a better weekend with my girlfriend",
        "Work on Open Project", "Teach EECS 281 Students",
        "Enjoy family time with my parents"
    ];
    tasks = [];
    for task_content in task_contents {
        task_info = Task(description = task_content by llm(method="Reason"));
        tasks.append(task_info);
    }
    print(tasks);
}