import base64, os, wave, openai

client = openai.Client(api_key=os.getenv("BOSON_API_KEY"), base_url="https://hackathon.boson.ai/v1")

messages = [
    {"role": "system", "content": "Convert the following text from the user into speech."},
    {"role": "user", "content": "Hello from Boson AI! Streaming to WAV test."},
]

stream = client.chat.completions.create(
    model="higgs-audio-generation-Hackathon",
    messages=messages,
    modalities=["text", "audio"],
    audio={"format": "pcm16"},  # request raw PCM16 chunks
    stream=True,
    max_completion_tokens=300,
)

wf = wave.open("streamed_tts.wav", "wb")
wf.setnchannels(1)        # mono
wf.setsampwidth(2)        # 16-bit PCM
wf.setframerate(24000)    # 24 kHz

try:
    for chunk in stream:
        delta = getattr(chunk.choices[0], "delta", None)
        audio = getattr(delta, "audio", None)
        if not audio:
            continue
        wf.writeframes(base64.b64decode(audio["data"]))
finally:
    wf.close()

print("Saved streamed audio to streamed_tts.wav")