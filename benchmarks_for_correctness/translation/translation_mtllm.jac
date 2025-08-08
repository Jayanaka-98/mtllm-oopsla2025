import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o");

glob examples: dict[str, str] = {
    "sea otter": "loutre de mer",
    "peppermint": "menthe poivrée",
    "plush giraffe": "girafe en peluche"
};

def translate(english_word: str) -> str by llm(incl_info=(examples));

with entry {
    import json;
    in_file = "/tmp/IN.json";
    with open(in_file) as f {
        data = json.load(f);
    }
    english_word = data["english_word"];
    print(translate(english_word));
}
