import from mtllm.llms {OpenAI}
import wikipedia;

glob llm = OpenAI(model_name="gpt-4o");

def get_wikipedia_summary(title: str) -> str {
    return wikipedia.summary(title);
}

def get_answer(question: str) -> str by llm(method="ReAct", tools=[get_wikipedia_summary]);

with entry {
    question = "Where is Apple Headquaters located?";
    import json;
    in_file = "/tmp/IN.json";
    with open(in_file) as f {
        data = json.load(f);
    }
    question = data["question"];
    answer = get_answer(question);
    print("Question:", question);
    print("Answer:", answer);
    # question = "Who is Elon Musk?";
    # answer = get_answer(question);
    # print("Question:", question);
    # print("Answer:", answer);
}
