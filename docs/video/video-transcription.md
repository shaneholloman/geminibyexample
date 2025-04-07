# Video transcription

This example demonstrates how to transcribe the content of a video using the Gemini API.
Note: For videos larger than 20MB, you must use the File API for uploading.

Import the Gemini API

```python
from google import genai
from google.genai import types
import os
import requests
```

Initialize the Gemini client with your API key

```python
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

video_url = "https://download.samplelib.com/mp4/sample-5s.mp4"
```

Download the video file.
Read the video file as bytes for inline upload.

```python
response = requests.get(video_url)
video_bytes = response.content
```

Define our prompt

```python
prompt = (
    "Transcribe the audio from this video, giving timestamps for "
    "salient events in the video. Also provide visual descriptions."
)
```

Create a Gemini request with the video and our prompt.

```python
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=types.Content(
        parts=[
            types.Part(text=prompt),
            types.Part(inline_data=types.Blob(data=video_bytes, mime_type="video/mp4")),
        ]
    ),
)
```

Print the model's response

```python
print(response.text)
```



## Running the Example

First, install the Google Generative AI library

```sh
$ pip install google-genai

```

Then run the program with Python

```sh
$ python video_transcription.py
Okay, here's the transcription and visual descriptions of the video:
**Video Description:**
The video pans up from a low angle showing a park with lush green trees.  Sunlight filters through the leaves. In the distance, cars and a bus can be seen on a road next to the park. There is a paved walkway and low bushes.
**Timestamps:**
*   **0:00** Camera starts panning up showing a park with trees and sunlight. 
*   **0:04** The camera reaches its highest point in its view.
```



## Further Information

- [Gemini docs link 1](https://ai.google.dev/gemini-api/docs/vision?lang=python#prompting-video)
