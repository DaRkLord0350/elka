from backend.api.query import ask_question

question = input("Enter your question: ")
response = ask_question(question)

print("\nANSWER:\n")
print(response)
