import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o");

enum Personality {
   INTROVERT = "Introvert",
   EXTROVERT = "Extrovert",
   Ambivert = "Ambivert",
}

obj Person {
    has full_name: str,
        yod: int,
        personality: Personality;
}

def get_person_info(name: str) -> Person by llm();

with entry {
    import json;
    in_file = "/tmp/IN.json";
    with open(in_file) as f {
        data = json.load(f);
    }
    name = data["name"];
    person_obj = get_person_info(name);
    print(f"{person_obj.full_name} was a {person_obj.personality.value} person who died in {person_obj.yod}");
}