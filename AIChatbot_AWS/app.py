from langchain.chains import LLMChain
from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
import boto3
import os
import streamlit as st


aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

bedrock_client = boto3.client(
    service_name = "bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key  
)


st.set_page_config(page_title="AI Chatbot", layout="centered")
st.title("Bedrock Chatbot")

model_id = st.sidebar.selectbox("Select Model", ["anthropic.claude-v2", "anthropic.claude-v3"])

llm = Bedrock(
    model_id=model_id,
    client=bedrock_client,
    model_kwargs={"max_tokens_to_sample": 2000, "temperature": 0.9}
)


def my_chatbot(freeform_text):
    prompt = PromptTemplate(
        input_variables=["freeform_text"],
        template="{freeform_text}"
    )
    bedrock_chain = LLMChain(llm=llm , prompt=prompt)
    response = bedrock_chain({'freeform_text': freeform_text})
    return response


st.sidebar.header("Chat Settings")
freeform_text = st.sidebar.text_area(
    label="Enter your question", 
    placeholder="Ask me anything...", 
    max_chars=300
)

if st.sidebar.button("Get Response") and freeform_text:
    with st.spinner("Generating response..."):
        response = my_chatbot(freeform_text)
    st.subheader("Response:")
    st.write(response['text'])
else:
    st.info("Please enter a question in the sidebar to get started.")

