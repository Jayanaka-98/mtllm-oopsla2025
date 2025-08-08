import dspy


llm = dspy.LM('openai/gpt-4o', cache=False, )

dspy.configure(lm=llm)

question = "Tobias is buying a new pair of shoes that costs $95. He has been saving up his money each month for the past three months. He gets a $5 allowance a month. He also mows lawns and shovels driveways. He charges $15 to mow a lawn and $7 to shovel. After buying the shoes, he has $15 in change. If he mows 4 lawns, how many driveways did he shovel?"
answer = dspy.TypedChainOfThought('question:str -> answer:int', max_retries=1)
response = answer(question=question)

print(response.answer)