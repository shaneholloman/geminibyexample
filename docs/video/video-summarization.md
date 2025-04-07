# Video summarization

This example demonstrates how to summarize the content of a video using the Gemini API.
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

Create a Gemini request with the video and a question

```python
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=types.Content(
        parts=[
            types.Part(text="Summarize the content of this video."),
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
$ python video_summarization.py
The video shows a park with trees next to a busy street with cars and buses passing by. The sun shines through the leaves of the trees.
```



## Further Information

- [Gemini docs link 1](https://ai.google.dev/gemini-api/docs/vision?lang=python#prompting-video)
