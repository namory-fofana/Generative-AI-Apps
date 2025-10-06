import streamlit as st
import assemblyai as aai
import os


# Replace with your API key
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

st.title("Audio Transcription App with AssemblyAI")
st.write("Upload your audio file (mp3 format) and get the transcription")

uploaded_file = st.file_uploader("Choose an audio mp3 file...", type=["mp3","mp4","wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3")  # display the audio file
    with open("temp_audio.mp3", "wb") as f:
        f.write(uploaded_file.getbuffer())  # write the file to the uploaded folder

    FILE_URL = "temp_audio.mp3"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL)

    if transcript.status == aai.TranscriptStatus.error:
        st.error(f"Error: {transcript.error}")
    else:
        st.subheader("Transcription:")
        st.write(transcript.text)
