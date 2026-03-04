from backend.api.query import ask_question

question = "What is my name & college name & project name?"
response = ask_question(question)

print("\nANSWER:\n")
print(response)
