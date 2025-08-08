import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o");

def get_suitable_expert(question: str) -> str by llm(method="Reason");
def get_answer_of_expert(question: str, expert: str) -> str by llm();

with entry {
    question = "What are Large Language Models?";
    import json;
    in_file = "/tmp/IN.json";

    with open(in_file) as f{
        data = json.load(f);
    }
    question= data["question"];
    expert = get_suitable_expert(question);
    answer = get_answer_of_expert(question, expert);
    print(f"{expert} says: '{answer}' ");
}
