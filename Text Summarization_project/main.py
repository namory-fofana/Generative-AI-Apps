import cohere
api=os.getenv("COHERE_API_KEY")
co = cohere.ClientV2(api)
response = co.chat(
    model="command-a-03-2025", 
    messages=[{"role": "user", "content": "hello world!"}]
)

print(response.message.content[0].text)
