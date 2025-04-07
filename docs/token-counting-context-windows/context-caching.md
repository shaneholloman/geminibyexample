# Context caching

This example demonstrates how to use the Gemini API's context caching feature to
efficiently query a large document multiple times without resending it with each request.
This can reduce costs when repeatedly referencing the same content.

```python
from google import genai
from google.genai.types import CreateCachedContentConfig, GenerateContentConfig
import os
import time
import requests
```

Initialize the Gemini client with your API key

```python
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```

Specify a versioned model that supports context caching
Note: Must use explicit version suffix (-001) for caching

```python
model_id = "gemini-1.5-flash-001"
```

Load a large document (e.g., technical documentation).
For this example, we assume the document is in markdown format.

```python
response = requests.get("https://zenml.io/llms.txt")
response.raise_for_status()  # Raise an exception for HTTP errors
api_docs = response.text
```

Create a cache with the document and system instructions

```python
cache = client.caches.create(
    model=model_id,
    config=CreateCachedContentConfig(
        display_name="ZenML LLMs.txt Documentation Cache",  # Used to identify the cache
        system_instruction=(
            "You are a technical documentation expert. "
            "Answer questions about the ZenML documentation provided. "
            "Keep your answers concise and to the point."
        ),
        contents=[api_docs],
        ttl="900s",  # Cache for 15 minutes
    ),
)
```

Display cache information

```python
print(f"Cache created with name: {cache.name}")
print(f"Cached token count: {cache.usage_metadata.total_token_count}")
print(f"Cache expires at: {cache.expire_time}")
```

Define multiple queries to demonstrate reuse of cached content

```python
queries = [
    "What are the recommended use cases for ZenML's pipeline orchestration?",
    "How does ZenML integrate with cloud providers?",
]
```

Run multiple queries using the same cached content

```python
for query in queries:
    print(f"\nQuery: {query}")
```

Generate response using the cached content

```python
response = client.models.generate_content(
        model=model_id,
        contents=query,
        config=GenerateContentConfig(cached_content=cache.name),
    )
```

Print token usage statistics to demonstrate savings

```python
print(f"Total tokens: {response.usage_metadata.total_token_count}")
    print(f"Cached tokens: {response.usage_metadata.cached_content_token_count}")
    print(f"Output tokens: {response.usage_metadata.candidates_token_count}")
```

Print the response (truncated for brevity)

```python
print(f"Response: {response.text}...")

    time.sleep(1)  # Short delay between requests
```

When done with the cache, you can delete it to free up resources

```python
client.caches.delete(name=cache.name)
```



## Running the Example

Install the Google Generative AI library

```sh
$ pip install google-genai

```

Run the Python script

```sh
$ python context-caching.py
Cache created with name: cachedContents/n8upgecthnz7
Cached token count: 107203
Cache expires at: 2025-04-05 20:21:48.818511+00:00
Query: What are the recommended use cases for ZenML's pipeline orchestration?
Total tokens: 107387
Cached tokens: 107203
Output tokens: 168
Response: ZenML's pipeline orchestration is well-suited for a wide range of machine learning workflows, including:
* **Data preprocessing:**  Ingesting, cleaning, transforming, and preparing data for model training.
* **Model training:**  Training various types of machine learning models, including deep learning models.
* **Model evaluation:**  Assessing model performance using different metrics and techniques.
* **Model deployment:**  Deploying trained models to different environments for inference.
* **Model monitoring:**  Monitoring the performance and health of deployed models in real-time.
* **A/B testing:**  Experimenting with different model variations and comparing their performance.
* **Hyperparameter tuning:**  Finding optimal hyperparameters for models.
* **Feature engineering:**  Developing and evaluating new features for improving model performance. 
...
Query: How does ZenML integrate with cloud providers?
Total tokens: 107326
Cached tokens: 107203
Output tokens: 113
Response: ZenML integrates with cloud providers by offering stack components that are specific to each provider, such as:
* **Artifact Stores:** S3 (AWS), GCS (GCP), Azure Blob Storage (Azure)
* **Orchestrators:** Skypilot (AWS, GCP, Azure), Kubernetes (AWS, GCP, Azure)
* **Container Registries:** ECR (AWS), GCR (GCP), ACR (Azure)
These components allow you to run pipelines on cloud infrastructure, enabling you to scale and leverage the benefits of cloud computing. 
...
```



## Further Information

- [Gemini docs link 1](https://ai.google.dev/gemini-api/docs/caching?lang=python)

- [Gemini docs link 2](https://ai.google.dev/api/caching)
