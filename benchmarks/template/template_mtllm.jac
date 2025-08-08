import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o");

obj Singer {
    has name: str, age: int, top_2_songs: list[str];
}

with entry {
    bruno_mars = Singer(name="Bruno Mars"by llm());
    print(f"{bruno_mars.name} is {bruno_mars.age} years old. His top 2 songs are {bruno_mars.top_2_songs}.");
}
