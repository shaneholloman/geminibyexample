# Embeddings generation

This example demonstrates generating text embeddings for cat-related terms using the Gemini API.

Import the Gemini API

```python
from google import genai
import os
```

Initialize the Gemini client with your API key

```python
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```

Specify the embedding model to use

```python
model_name = "gemini-embedding-exp-03-07"
```

Define some cat-related terms

```python
cats = ["Siamese cat", "Persian cat", "cat food", "cat nap"]
```

Generate embeddings for each term

```python
embeddings = []
for cat in cats:
    result = client.models.embed_content(model=model_name, contents=cat)
    embeddings.append(result.embeddings)
```

Print the embeddings (for demonstration purposes, showing the length)

```python
for i, embedding in enumerate(embeddings):
    embedding_values = embedding[0].values
    print(f"Embedding for '{cats[i]}': Length = {len(embedding_values)}")
    print(f"First 10 values: {embedding_values[0:10]}")
```



## Running the Example

First, install the Google Generative AI library

```sh
$ pip install google-generative-ai

```

Then run the program with Python

```sh
$ python embeddings_example.py
Embedding for 'Siamese cat': Length = 3072
First 10 values: [-0.04499451, -0.0024065399, 0.00653481, -0.079863556, -0.03341567, 0.016723568, 0.010078963, -0.012704449, -0.012259528, -0.0072885454]
Embedding for 'Persian cat': Length = 3072
First 10 values: [-0.043987285, 0.033221565, 0.0016907051, -0.056972563, 0.006436907, -0.0006723535, -0.0009717501, 0.033097122, -6.910255e-05, -0.017573195]
Embedding for 'cat food': Length = 3072
First 10 values: [-0.025519634, 0.013711145, 0.045626495, -0.055266093, 0.002371603, 0.01668532, -0.022395907, 0.0109309815, 0.026964031, 0.027647937]
Embedding for 'cat nap': Length = 3072
First 10 values: [-0.024834476, 0.009304642, -0.003533542, -0.08721581, -0.0068027894, 0.003322256, 0.01155771, 0.027575387, 0.012308658, -0.013031868]
```



## Further Information

- [Gemini docs link 1](https://ai.google.dev/gemini-api/docs/embeddings)

- [Gemini docs link 2](https://ai.google.dev/gemini-api/docs/embeddings#resthttps://ai.google.dev/gemini-api/docs/embeddings#resthttps://ai.google.dev/gemini-api/docs/embeddings#rest)
