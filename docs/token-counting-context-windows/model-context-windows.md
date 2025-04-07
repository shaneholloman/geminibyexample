# Model context windows

This example demonstrates how to access the input and output token limits for different Gemini models.

Import the Gemini API

```python
from google import genai
import os
```

Configure the client with your API key

```python
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```

Get information about the gemini-2.0-flash model

```python
model_info = client.models.get(model="models/gemini-2.0-flash")
```

Print the input and output token limits for gemini-2.0-flash

```python
print("Gemini 2.0 Flash:")
print(
    f"  Input token limit: {model_info.input_token_limit:,} tokens (1 million tokens)"
)
print(
    f"  Output token limit: {model_info.output_token_limit:,} tokens (8 thousand tokens)"
)
```

Get information about the gemini-2.5-pro-preview-03-25 model

```python
pro_model_info = client.models.get(model="models/gemini-2.5-pro-preview-03-25")
```

Print the input and output token limits for gemini-2.5-pro-preview-03-25

```python
print("\nGemini 2.5 Pro:")
print(
    f"  Input token limit: {pro_model_info.input_token_limit:,} tokens (1 million tokens)"
)
print(
    f"  Output token limit: {pro_model_info.output_token_limit:,} tokens (65 thousand tokens)"
)
```



## Running the Example

First, install the Google Generative AI library

```sh
$ pip install google-genai

```

Then run the program with Python

```sh
$ python model_context.py
Gemini 2.0 Flash:
  Input token limit: 1,048,576 tokens (1 million tokens)
  Output token limit: 8,192 tokens (8 thousand tokens)
Gemini 2.5 Pro:
  Input token limit: 1,048,576 tokens (1 million tokens)
  Output token limit: 65,536 tokens (65 thousand tokens)
```



## Further Information

- [Gemini docs link 1](https://ai.google.dev/gemini-api/docs/tokens?lang=python)
