# LiteLLM

This example demonstrates how to use the LiteLLM library to make calls to the
Gemini API.
It shows a simple text generation call and then shows structured output using
a Pydantic model.

Import the necessary libraries. Make sure that LiteLLM and Pydantic are installed.

```python
from litellm import completion
from pydantic import BaseModel
import json
```

With this first example, we'll make a simple text generation call.

```python
response = completion(
    model="gemini/gemini-2.0-flash-lite",
    messages=[{"role": "user", "content": "Hello what is your name?"}],
)
print(response.choices[0].message.content)
```

Now let's define a slightly more involved example that defines a Pydantic
model and uses it to specify the response format.

```python
class Response(BaseModel):
    response: str
    good_response: bool
```

We'll use the same prompt as before, but this time we'll specify that the
response should be a JSON object that matches the Response model.

```python
response = completion(
    model="gemini/gemini-2.0-flash-lite",
    messages=[{"role": "user", "content": "Hello what is your name?"}],
    response_format={
        "type": "json_object",
        "response_schema": Response.model_json_schema(),
    },
)
```

The response is a JSON object that matches the Response model.

```python
print(json.loads(response.choices[0].message.content))
```



## Running the Example

First, install the LiteLLM and Pydantic libraries

```sh
$ pip install litellm pydantic

```

Then run the program with Python

```sh
$ python litellm.py
I am a large language model, trained by Google. I don't have a name in the traditional sense. You can just call me by what I am!
{'good_response': False, 'response': "I am a large language model, I don't have a name."}
```



## Further Information

- [Gemini docs link 1](https://litellm.vercel.app/docs/providers/gemini)
