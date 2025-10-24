# Boson AI API Hackathon Tutorials

## Before Start
Checkout the following links:
* [Higgs Audio V2 Blog](https://www.boson.ai/blog/higgs-audio-v2)
* [Higgs Audio V2 Github Repo](https://github.com/boson-ai/higgs-audio)
* [Higgs Audio V2 Huggingface Repo](https://huggingface.co/bosonai/higgs-audio-v2-generation-3B-base)
* [Higgs Audio V2 Huggingface Playground](https://huggingface.co/spaces/smola/higgs_audio_v2) 

## API Key

Your API key is a unique identifier that allows you to access the Boson AI API.

Export the API key to the environment variable `BOSON_API_KEY` for use in the following examples.

```bash
export BOSON_API_KEY=****
```

## Endpoints

- `https://hackathon.boson.ai/v1` OpenAI-compatible API, for text, audio understanding and audio generation.

## Text endpoint

Boson provides OpenAI-compatible chat completion API with the following models:
- higgs-audio-generation-Hackathon
- Qwen3-32B-thinking-Hackathon
- Qwen3-32B-non-thinking-Hackathon
- Qwen3-14B-Hackathon
- higgs-audio-understanding-Hackathon
- Qwen3-Omni-30B-A3B-Thinking-Hackathon


### cURL Example

```bash
curl -X POST "https://hackathon.boson.ai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BOSON_API_KEY" \
  -d '{
    "model": "Qwen3-32B-thinking-Hackathon",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "max_tokens": 128,
    "temperature": 0.7
  }'
```

### Python Example
```python
import openai
import os

BOSON_API_KEY = os.getenv("BOSON_API_KEY")

client = openai.Client(
    api_key=BOSON_API_KEY,
    base_url="https://hackathon.boson.ai/v1"
)

response = client.chat.completions.create(
    model="<Model>", # replace it
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum physics briefly."}
    ],
    max_tokens=128,
    temperature=0.7
)

print(response.choices[0].message.content)
```

For detailed API documentation and additional parameters, refer to the [OpenAI API documentation](https://platform.openai.com/docs/api-reference/chat).

## Audio understanding endpoint

Boson provides audio understanding capabilities(general understanding, audio transcription, audio chat) through the chat completions API using the `higgs-audio-understanding` model. It supports various audio formats (mp3, wav, etc.) with base64 encoding.

### cURL Example
```bash
# First, encode your audio file to base64
AUDIO_BASE64=$(base64 -i /path/to/your/audio.wav)

curl -X POST "https://hackathon.boson.ai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BOSON_API_KEY" \
  -d '{
    "model": "higgs-audio-understanding-Hackathon",
    "messages": [
      {"role": "system", "content": "Transcribe the audio."},
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {
              "data": "'$AUDIO_BASE64'",
              "format": "wav"
            }
          }
        ]
      }
    ],
    "max_completion_tokens": 256,
    "temperature": 0.0
  }'
```

### Python Example
```python
import openai
import base64
import os

BOSON_API_KEY = os.getenv("BOSON_API_KEY")

def encode_audio_to_base64(file_path: str) -> str:
    """Encode audio file to base64 format."""
    with open(file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")

client = openai.Client(
    api_key=BOSON_API_KEY,
    base_url="https://hackathon.boson.ai/v1"
)

# Transcribe audio
audio_path = "/path/to/your/audio.wav"
audio_base64 = encode_audio_to_base64(audio_path)
file_format = audio_path.split(".")[-1]

response = client.chat.completions.create(
    model="higgs-audio-understanding-Hackathon",
    messages=[
        {"role": "system", "content": "Transcribe this audio for me."},
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": audio_base64,
                        "format": file_format,
                    },
                },
            ],
        },
    ],
    max_completion_tokens=256,
    temperature=0.0,
)

# Chat about the audio
audio_path = "/path/to/your/audio.wav"
audio_base64 = encode_audio_to_base64(audio_path)
file_format = audio_path.split(".")[-1]

response = client.chat.completions.create(
    model="higgs-audio-understanding-Hackathon",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": audio_base64,
                        "format": file_format,
                    },
                },
            ],
        },
        {
            "role": "user",
            "content": "Is it a male's voice or female's?",
        },
    ],
    max_completion_tokens=256,
    temperature=0.0,
)

print(response.choices[0].message.content)
```


### Usage notes & best practices
* The model can also act as a general-purpose chat model. It can understand users' questions and directly generate text responses. System prompt and temperature could matter a lot.
* For detailed API documentation and additional parameters, refer to the [OpenAI API documentation](https://platform.openai.com/docs/api-reference/chat).

## Audio generation endpoint

Boson provides speech generation capabilities using the `higgs-audio-generation-Hackathon` model via the `audio/speech` endpoint with two different endpoint formats:

### 1. Simple Generation

This is the simplest way to call the model. Similar to OpenAI's speech API, supports voices: `belinda`, `broom_salesman`, `chadwick`, `en_man`, `en_woman`, `mabel`, `vex`, `zh_man_sichuan`

#### cURL Example
```bash
curl -X POST "https://hackathon.boson.ai/v1/audio/speech" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BOSON_API_KEY" \
  -d '{
    "model": "higgs-audio-generation-Hackathon",
    "voice": "en_woman_1",
    "input": "Today is a wonderful day to build something people love!",
    "response_format": "pcm"
  }' \
  --output speech.pcm && ffplay -f s16le -ar 24000 speech.pcm
```

#### Python Example
```python
import openai
import os
import wave


BOSON_API_KEY = os.getenv("BOSON_API_KEY")

client = openai.Client(
    api_key=BOSON_API_KEY,
    base_url="https://hackathon.boson.ai/v1"
)

# for this api, we onlu support PCM format output
response = client.audio.speech.create(
    model="higgs-audio-generation-Hackathon",
    voice="belinda",
    input="Hello, this is a test of the audio generation system.",
    response_format="pcm"
)

# You can use these parameters to write PCM data to a WAV file
num_channels = 1        
sample_width = 2        
sample_rate = 24000   

pcm_data = response.content

with wave.open('belinda_test.wav', 'wb') as wav:
    wav.setnchannels(num_channels)
    wav.setsampwidth(sample_width)
    wav.setframerate(sample_rate)
    wav.writeframes(pcm_data)

```

For detailed API documentation and additional parameters, refer to the [OpenAI API documentation](https://platform.openai.com/docs/api-reference/audio).

### 2. Generation with more controlment

This example uses chat completions with reference audio for in-context voice cloning capabilities. Please make sure the content of the reference audio must align with the content of the user's message. The following script dumps a `.wav` file.

```python
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

resp = client.chat.completions.create(
    model="higgs-audio-generation-Hackathon",
    messages=[
        {"role": "user", "content": reference_transcript},
        {
            "role": "assistant",
            "content": [{
                "type": "input_audio",
                "input_audio": {"data": b64(reference_path), "format": "wav"}
            }],
        },
        {"role": "user", "content": "Welcome to Boson AI's voice generation system."},
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
```

Also we provide another voice-cloning prompt template. Checkout the `cloning_example.py` file in this repo. You are also welcome to try you own prompt. 

### Usage notes & best practices
* We provide several ref-voices in ./ref-aduio, you can also try other voices.
* Use system prompt or scene description to control. E.g. *'<|scene_desc_start|> Audio is recorded from a quiet room. <|scene_desc_end|>'*
* There is a trade-off between expressiveness and robustness. Try to use settings such as temperature, top_p, and top_k to balance. Specify the maximum token length (e.g., max_new_tokens) to limit output size. Provide stop strings (e.g., "<|end_of_text|>", "<|eot_id|>") to signal when the generation should finish. You can try to adjust any parameters as you want.
* Sometimes the model will hallucinate and generate a noise much longer than expected. Believe us, we are improving on this for the next release lol. Please keep following our [website](https://www.boson.ai/).

## Qwen3-Omni (multimodal)

**What it is:** Qwen3-Omni supports **text, image, audio, and video** inputs.
Use **Qwen3-Omni-30B-A3B-Thinking** when you need strongest multimodal reasoning with **text-only output**. 

> Tip: Include an explicit textual instruction alongside your media (e.g., “analyze this audio + image together”) to improve reasoning quality. ([Hugging Face][1])

### Multimodal chat (cURL)

```bash
curl -X POST "https://hackathon.boson.ai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BOSON_API_KEY" \
  -d '{
    "model": "Qwen3-Omni-30B-A3B-Thinking-Hackathon",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": [
        {"type": "image_url", "image_url": {"url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-Omni/demo/cars.jpg"}},
        {"type": "audio_url", "audio_url": {"url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-Omni/demo/cough.wav"}},
        {"type": "text", "text": "Describe what you see and what you hear in one sentence."}
      ]}
    ],
    "max_tokens": 256,
    "temperature": 0.2
  }'
```

This uses the **OpenAI-style multimodal message format** (`image_url`, `audio_url`) exactly as shown in the model documentation. ([Hugging Face][1])

### Multimodal chat (Python)

```python
import os, openai
client = openai.Client(api_key=os.getenv("BOSON_API_KEY"),
                       base_url="https://hackathon.boson.ai/v1")

resp = client.chat.completions.create(
    model="Qwen3-Omni-30B-A3B-Thinking-Hackathon",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {
                "url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-Omni/demo/cars.jpg"}},
            {"type": "audio_url", "audio_url": {
                "url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-Omni/demo/cough.wav"}},
            {"type": "text", "text": "Summarize what the image shows and what the audio sounds like."}
        ]}
    ],
    max_tokens=256,
    temperature=0.2,
)
print(resp.choices[0].message.content)
```

The **Thinking** model accepts audio/image/video inputs but **returns text**.

### Usage notes & best practices

* **Explicit instruction helps.** Provide a short task description alongside media each turn (e.g., “analyze this audio, image, and video together”). ([Hugging Face][1])
* **Video with audio:** isn’t available, so pass video and audio **separately** and keep handling consistent across turns. ([Hugging Face][1])

**References:** Hugging Face model cards for **Thinking** and **Instruct** include full QuickStart, multimodal message examples, vLLM notes, and best-practice prompts. ([Hugging Face][1])

[1]: https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Thinking "Qwen/Qwen3-Omni-30B-A3B-Thinking · Hugging Face"
