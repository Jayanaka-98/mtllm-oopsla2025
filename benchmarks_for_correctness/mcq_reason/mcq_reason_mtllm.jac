import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o");

def get_answer_key(question: str, choices: dict) -> str by llm(method="Chain-of-Thoughts");

with entry {
    question: str = "It was Sept. 1st, 2021 a week ago. What is the date 10 days ago in MM/DD/YYYY?";
    choices: dict = { "A": "08/29/2021", "B": "08/28/2021", "C": "08/29/1925", "D": "08/30/2021", "E": "05/25/2021", "F": "09/19/2021"};
    import json;
    in_file = "/tmp/IN.json";
    with open(in_file) as f {
        data = json.load(f);
    }
    question = data["question"];
    choices = data["choices"];
    print(get_answer_key(question, choices));
}