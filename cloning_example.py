from openai import OpenAI
import base64
import os

BOSON_API_KEY = os.getenv("BOSON_API_KEY")
client = OpenAI(api_key=BOSON_API_KEY, base_url="https://hackathon.boson.ai/v1")

def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode("utf-8")

reference_path = "./ref-audio/hogwarts_wand_seller_v2.wav"
reference_transcript = (
    "I would imagine so. A wand with a dragon heartstring core is capable of dazzling magic. "
    "And the bond between you and your wand should only grow stronger. Do not be surprised at your new "
    "wand's ability to perceive your intentions - particularly in a moment of need."
)

system = (
    "You are an AI assistant designed to convert text into speech.\n"
    "If the user's message includes a [SPEAKER*] tag, do not read out the tag and generate speech for the following text, using the specified voice.\n"
    "If no speaker tag is present, select a suitable voice on your own.\n\n"
    "<|scene_desc_start|>\nAudio is recorded from a quiet room.\n<|scene_desc_end|>"
)

resp = client.chat.completions.create(
    model="higgs-audio-generation-Hackathon",
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": reference_transcript},
        {
            "role": "assistant",
            "content": [{
                "type": "input_audio",
                "input_audio": {"data": b64(reference_path), "format": "wav"}
            }],
        },
        {"role": "user", "content": "[SPEAKER0] Welcome to Boson AI's voice generation system."},
    ],
    modalities=["text", "audio"],
    max_completion_tokens=4096,
    temperature=1.0,
    top_p=0.95,
    stream=False,
    stop=["<|eot_id|>", "<|end_of_text|>", "<|audio_eos|>"],
    extra_body={"top_k": 50},
)

audio_b64 = resp.choices[0].message.audio.data
open("output.wav", "wb").write(base64.b64decode(audio_b64))