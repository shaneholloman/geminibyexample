# Rate limits and retries

This example demonstrates generating text with the Gemini API, handling rate limiting errors, and using exponential backoff for retries.

```python
import google.generativeai as genai
import google.ai.generativelanguage as glm
import time
import os
```

Configure the retry strategy

```python
def configure_retries(base_delay=1, max_delay=60, max_retries=5):
    """Configures exponential backoff retry strategy."""
    return genai.retry.RetryConfig(
        initial_delay=base_delay,
        max_delay=max_delay,
        max_retries=max_retries,
        retry_on_status_codes=[glm.Code.RESOURCE_EXHAUSTED.value],
    )
```

Set the retry configuration

```python
retry_config = configure_retries()
```

Initialize the Gemini client with your API key

```python
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY"), retry_config=retry_config
)
```

Select the model

```python
model = "gemini-2.0-flash"
```

Construct the prompt

```python
prompt = "Tell me a funny story about a cat trying to catch a laser pointer."
```

Attempt text generation with retry logic


```python
try:
    response = client.models.generate_content(model=model, contents=prompt)
    print(response.text)
except genai.errors.APIError as e:
    print(f"An error occurred: {e}")
```



## Running the Example

First, install the Google Generative AI library

```sh
$ pip install google-genai backoff

```

Then run the program with Python

```sh
$ python text_generation_with_retry.py
Bartholomew Buttersworth the Third, a cat of considerable fluff and even more considerable ego, considered himself a master predator. His domain, the living room, was usually ruled with a sleepy, regal disdain.
Until the Red Dot appeared.
It materialized silently on the beige carpet, an insolent crimson speck challenging his authority. Bartholomew's eyes, previously half-closed slits of judgment, snapped wide open. His tail gave an involuntary *thwack* against the armchair.
*Prey.*
He crouched low, hindquarters wiggling with suppressed energy, a furry missile preparing for launch. The dot danced teasingly towards the sofa leg. Bartholomew *pounced!*
He landed with an ungraceful *floof* exactly where the dot *had* been. It was now, infuriatingly, halfway up the wall.
Bartholomew stared, blinked, and launched himself vertically. His claws scrabbled momentarily against the paint before gravity asserted its dominance. He slid down the wall with a soft *scritch-scratch-thump*.
The dot, utterly unimpressed, zipped across the ceiling. Bartholomew tracked it, head tilting back so far he nearly somersaulted. He tried a running leap off the coffee table, misjudged the trajectory entirely, and ended up skidding under the armchair, emerging moments later covered in dust bunnies and indignation.
The dot, meanwhile, had settled innocently on his own fluffy white paw.
Bartholomew froze. Victory? He stared at the dot. The dot stared back (metaphorically speaking). Slowly, cautiously, he brought his nose down to sniff the intruder...
*Click.*
The dot vanished.
Bartholomew looked at his paw. He looked around the room, eyes wide with betrayal. Where did it go? Was it *inside* his paw? He bit his paw gently, then shook his head, utterly bewildered.
Finally, defeated and slightly dizzy, Bartholomew stalked over to his food bowl, pretending the entire embarrassing episode had never happened. The Red Dot, however, remained an unsolved mystery, a tiny, mocking ghost in his otherwise perfect predatory world.
```



## Further Information

- [Gemini docs link 1](https://ai.google.dev/gemini-api/docs/text-generation)

- [Gemini docs link 2](https://ai.google.dev/gemini-api/docs/troubleshooting?lang=python)

- [Gemini docs link 3](https://ai.google.dev/gemini-api/docs/rate-limits?hl=en)
