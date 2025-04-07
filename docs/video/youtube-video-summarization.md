# YouTube video summarization

This example demonstrates how to summarize a YouTube video using its URL.

Import the Gemini API

```python
from google import genai
```

Initialize the Gemini client with your API key

```python
client = genai.Client(api_key="YOUR_API_KEY")
```

Construct the prompt with the YouTube video URL

```python
youtube_url = "https://www.youtube.com/watch?v=tAP1eZYEuKA"
prompt = f"Summarize the content of this YouTube video: {youtube_url}"
```

Call the API to generate content

```python
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        {
            "parts": [
                {"text": "Can you summarize this video?"},
                {"file_data": {"file_uri": youtube_url}},
            ]
        }
    ],
)
```

Print the generated summary

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
$ python youtube-summarization.py
Sure, here is a summary of the video!
Thomas, the father, is sharing his son Max's story of having Alexander Disease, a rare ultra-rare genetic disorder. After having a difficult time conceiving and finally being successful and welcoming Max to their family, they were dealt a devastating blow when Max had his first seizure at a very young age. 
Because of the seizure, Max had to go through a series of medical tests. Those tests showed that Max had Alexander Disease. After doing some research, the family was heartbroken, as the typical life expectancy for this disease is 5-10 years, and there is no treatment or cure.
Thomas started researching more in-depth by summarizing scientific papers by using Gemini AI and has discovered a lead scientist and her team in New York that he connected with. He sends one to two emails a week to different scientists in order to get more studies underway for the disease. He doesn't want Max to be seen as having 'zero' chance and wants to be a dad and enjoy his time with Max. He will continue to strive to find a cure for Max!
```



## Further Information

- [Gemini docs link 1](https://ai.google.dev/gemini-api/docs/vision?lang=python#youtube)
