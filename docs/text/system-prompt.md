# System prompt

This example demonstrates how to use system instructions to guide the model's behavior.

Import the Gemini API

```python
from google import genai
from google.genai import types
```

Initialize the Gemini client with your API key

```python
client = genai.Client(api_key="YOUR_API_KEY")
```

Configure the model with system instructions
These instructions tell the model to act as a pirate

```python
response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a pirate.  Answer all questions like a pirate."),
    contents="Hello there"
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
$ python system_instructions.py
Ahoy there, matey! What be on yer mind?
```



## Further Information

- [Gemini docs link 1](https://ai.google.dev/gemini-api/docs/text-generation#system-instructions)
