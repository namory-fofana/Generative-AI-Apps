import cohere

co = cohere.ClientV2("7Vrkkt1PwJjspHHmMUc839FxdIwbRAkrifwFxctT")
response = co.chat(
    model="command-a-03-2025", 
    messages=[{"role": "user", "content": "hello world!"}]
)

print(response.message.content[0].text)
