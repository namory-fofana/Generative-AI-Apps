from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
import streamlit as st
import threading
import uvicorn
import requests

# --- Initialisation FastAPI ---
app = FastAPI()

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste les origines si besoin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- OpenAI client ---
# Assure-toi que OPENAI_API_KEY est défini dans ton environnement
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Pydantic model ---
class Request(BaseModel):
    prompt: str

# --- Endpoint pour générer du texte ---
@app.post("/generate")
async def generate_content(request: Request):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": request.prompt}]
        )
        ai_response = completion.choices[0].message.content
        return {"response": ai_response}
    except Exception as e:
        return {"error": str(e)}

# --- Lancer FastAPI dans un thread ---
def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000)

# --- App Streamlit ---
def run_streamlit():
    st.title("AI Content Generator")
    st.write("Enter a prompt to generate content.")

    API_URL = "http://localhost:8000/generate"

    # Zone de saisie utilisateur
    user_input = st.text_area("Enter your prompt:")

    if st.button("Generate"):
        if user_input.strip():
            with st.spinner("Generating..."):
                try:
                    response = requests.post(API_URL, json={"prompt": user_input})
                    if response.status_code == 200:
                        result = response.json()
                        if "response" in result:
                            st.subheader("Generated Content")
                            st.write(result["response"])
                        else:
                            st.error(f"Error: {result.get('error', 'Unknown error')}")
                    else:
                        st.error(f"Error: Unable to contact API. Status code {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a prompt before clicking Generate.")

# --- Main ---
if __name__ == "__main__":
    # Lancer FastAPI dans un thread séparé
    api_thread = threading.Thread(target=run_fastapi, daemon=True)
    api_thread.start()

    # Lancer Streamlit
    run_streamlit()
