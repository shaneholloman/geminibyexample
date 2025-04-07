# Streaming text

This example demonstrates how to use the Gemini API to generate text content and stream the output.

Import the Gemini API

```python
from google import genai
```

Initialize the Gemini client with your API key

```python
client = genai.Client(api_key="YOUR_API_KEY")
```

Call the API to generate content in streaming mode

```python
response = client.models.generate_content_stream(
    model="gemini-2.0-flash",
    contents=["Explain how AI works"]
)
```

Iterate over the stream of responses and print each chunk of text

```python
for chunk in response:
    print(chunk.text, end="")
```



## Running the Example

First, install the Google Generative AI library

```sh
$ pip install google-genai

```

Then run the program with Python

```sh
$ python streaming-generation.py
AI, or Artificial Intelligence, is a broad field of computer science focused on creating machines capable of performing tasks that typically require human intelligence. It involves developing algorithms and models that enable computers to learn from data, reason, solve problems, understand natural language, perceive their environment, and make decisions.
AI can be achieved through various techniques, including:
*   **Machine Learning (ML):** This is a core subfield of AI where machines learn from data without being explicitly programmed. ML algorithms can identify patterns, make predictions, and improve their performance over time with more data.
*   **Deep Learning (DL):** A subfield of ML that uses artificial neural networks with multiple layers (deep neural networks) to analyze data and extract complex features. DL has been highly successful in areas like image recognition, natural language processing, and speech recognition.
*   **Natural Language Processing (NLP):** Focuses on enabling computers to understand, interpret, and generate human language. NLP techniques are used in applications like chatbots, machine translation, and sentiment analysis.
*   **Computer Vision:** Enables computers to "see" and interpret images and videos. Computer vision algorithms can identify objects, recognize faces, and analyze scenes.
*   **Robotics:** Involves designing, constructing, operating, and applying robots. AI is often used in robotics to enable robots to perform tasks autonomously.
AI is transforming various industries, including healthcare, finance, transportation, and manufacturing. It has the potential to solve complex problems and improve people's lives, but it also raises ethical and societal concerns that need to be addressed.
```



## Further Information

- [Gemini docs link 1](https://ai.google.dev/gemini-api/docs/text-generation)
