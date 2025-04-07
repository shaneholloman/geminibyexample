# Structured output

This example shows how to generate structured data using a pydantic model to represent Cats with name, colour, and special ability.

Import the Gemini API and pydantic

```python
from google import genai
from pydantic import BaseModel
import os
```

Define a Pydantic model for a Cat

```python
class Cat(BaseModel):
    name: str
    colour: str
    special_ability: str
```

Initialize the Gemini client with your API key

```python
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```

Define the prompt. Note: It asks for 3 cats

```python
prompt = "Generate data for 3 cats, including their name, colour and special ability."
```

Call the API to generate content, specifying the response schema.
Note that it expects a `list` and not a `typing.List` object.
For some reason Gemini models are finicky about that.

```python
response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": list[Cat],
    },
)
```

Parse the json response to a list of Cat objects

```python
my_cats: list[Cat] = response.parsed
```

Print the generated cat data

```python
for cat in my_cats:
    print(
        f"Name: {cat.name}, Colour: {cat.colour}, Special Ability: {cat.special_ability}"
    )
```



## Running the Example

First, install the Google Generative AI library and pydantic

```sh
$ pip install google-genai pydantic

```

Then run the program with Python

```sh
$ python structured_cats.py
Name: Aria, Colour: tortoiseshell, Special Ability: Can teleport short distances
Name: Blupus, Colour: ginger, Special Ability: Understands human speech
Name: Moonshine, Colour: black and white, Special Ability: Invisible at night
```



## Further Information

- [Gemini docs link 1](https://ai.google.dev/gemini-api/docs/structured-output?lang=python)

- [Gemini docs link 2](https://ai.google.dev/gemini-api/docs/structured-output?lang=rest)
