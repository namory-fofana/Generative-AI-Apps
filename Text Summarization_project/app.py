import cohere 
import streamlit as st
import os

#Initialize cohere client
cohere_api_key =os.getenv("COHERE_API_KEY")
co = cohere.ClientV2(api_key=cohere_api_key)

#Streamlit UI
st.title("Text Summarization with Cohere")

st.write("This app uses Cohere's API to summarize text. Enter the text you want to summarize below:")

#text input from user
user_input = st.text_area("Enter text  here:", height = 300)

if st.button("Summarize"):
    if user_input.strip():
        with st.spinner("Summarizing..."):
            try:
                #prepare the message for cohere
                message = f"Generate a concise and easy-to-understand summary of the following text, keeping only the key ideas:{user_input}"

                #call cohere API
                response = co.chat(
                    model="command-a-03-2025", 
                    messages=[{"role": "user", "content": message}]
                )

                #display summarized text
                summary = response.message.content[0].text
                st.subheader("Summarized text:")
                st.write(summary)

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some text to summarize.")

