import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4");

def joke_punchline() -> tuple[str, str] by llm();

with entry {
    (joke, punchline) = joke_punchline();
    print(f"{joke}: {punchline}");
}