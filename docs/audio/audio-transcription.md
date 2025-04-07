# Audio transcription

This example demonstrates how to transcribe an audio file by providing the audio data inline with the request.

Import the necessary modules

```python
from google import genai
from google.genai import types
import requests
```

Initialize the Gemini client with your API key

```python
client = genai.Client(api_key="YOUR_API_KEY")
```

Define a descriptive User-Agent following Wikimedia's policy

```python
user_agent = "GeminiByExample/1.0 (https://github.com/strickvl/geminibyexample; contact@example.org) python-requests/2.0"
```

Download the audio file from the URL

```python
url = "https://upload.wikimedia.org/wikipedia/commons/1/1f/%22DayBreak%22_with_Jay_Young_on_the_USA_Radio_Network.ogg"
headers = {"User-Agent": user_agent}
response = requests.get(url, headers=headers)
response.raise_for_status()  # Raise an exception for bad status codes
```

Read the audio file as bytes
Note: If your audio file is larger than 20MB, you should use the File API to upload the file first.
The File API allows you to upload larger files and then reference them in your requests.

```python
audio_bytes = response.content
```

Call the API to generate a transcription of the audio clip

```python
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        "Transcribe this audio clip",
        types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/ogg",
        ),
    ],
)
```

Print the transcribed text

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
$ python audio-transcription.py
We're joined once again by our travel expert and also author of America's Top Roller Coasters and Amusement Parks, Pete Trabucco. Good morning and welcome back to Daybreak USA. Well, thanks for having me on. If someone's lucky enough to go on vacation to an exotic location, and then maybe not so lucky to have some kind of a disaster happen while they're there, maybe some civil unrest. What should they do now? What's the next step? Well, whenever you're going on vacation whether it's locally or internationally, you've got to be uh very careful.
```



## Further Information

- [Gemini docs link 1](https://ai.google.dev/gemini-api/docs/audio?lang=python)
