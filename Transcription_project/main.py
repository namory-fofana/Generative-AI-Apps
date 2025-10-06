# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)
import os

import assemblyai as aai

aai.settings.api_key =  os.getenv("ASSEMBLY_AI_API_KEY")
transcriber = aai.Transcriber()

transcript = transcriber.transcribe("https://assembly.ai/news.mp4")
# transcript = transcriber.transcribe("./my-local-audio-file.wav")

print(transcript.text)