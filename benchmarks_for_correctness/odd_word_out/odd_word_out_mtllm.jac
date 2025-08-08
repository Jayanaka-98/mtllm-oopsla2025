import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o");

def get_reason_and_oddword(options: list[str]) -> tuple[str, str] by llm();

with entry {
    import json;
    in_file = "/tmp/IN.json";
    with open(in_file) as f {
        data = json.load(f);
    }
    print(get_reason_and_oddword(data["options"]));
}
