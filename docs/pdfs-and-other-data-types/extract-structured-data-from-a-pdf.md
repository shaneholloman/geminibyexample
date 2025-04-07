# Extract structured data from a PDF

This example demonstrates how to extract structured data from a PDF invoice using the Gemini API and Pydantic.

Import necessary libraries. You'll need Pydantic for this one.

```python
import os
import requests
import json
import re
from pydantic import BaseModel, Field
from typing import List, Union
from google import genai
from google.genai import types
```

Define Pydantic models for structured data

```python
class Item(BaseModel):
    name: str
    price_per_kg: Union[float, str] = Field(..., alias="price/kg")
    quantity_kg: Union[float, int] = Field(..., alias="quantity (kg)")


class InvoiceContents(BaseModel):
    sender: str
    recipient: str
    address: str
    full_total: Union[float, str]
    subtotal: Union[float, str]
    gst_value: Union[float, str] = Field(..., alias="GST")
    items: List[Item]
```

Load the PDF invoice inline from a URL.
For PDFs larger than 20MB, you'll need to use the Files API for uploading

```python
pdf_url = "https://www.princexml.com/samples/invoice/invoicesample.pdf"
response = requests.get(pdf_url)
response.raise_for_status()  # Ensure the download was successful
pdf_data = response.content
```

Initialize the Gemini client with your API key

```python
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY"))
```

Configure the model for structured output.
Specify the prompt text.

```python
model = "gemini-2.5-pro-preview-03-25"
prompt_text = (
    "Extract the following information from the invoice: "
    "sender, recipient, address, full_total, subtotal, GST, "
    "and a list of items (name, price/kg, quantity (kg))."
)
```

Call the Gemini API to extract structured data from the PDF

```python
response = client.models.generate_content(
    model=model,
    contents=[
        types.Part.from_bytes(data=pdf_data, mime_type="application/pdf"),
        prompt_text,
    ],
    config=genai.types.GenerateContentConfig(temperature=0.0),
)
```

Extract JSON from response text which might be formatted as a markdown code block.
Check if the response is a markdown code block and extract the JSON content.

```python
response_text = response.text
json_match = re.search(r"```(?:json)?\n(.*?)```", response_text, re.DOTALL)
if json_match:
    json_str = json_match.group(1).strip()
else:
    json_str = response_text.strip()
```

Parse the JSON response into the Pydantic model

```python
invoice_data = json.loads(json_str)
invoice = InvoiceContents(**invoice_data)
```

Print the extracted data as a JSON string

```python
print(invoice.model_dump_json(indent=2))
```



## Running the Example

Install the Google Generative AI library and Pydantic

```sh
$ pip install google-genai pydantic requests

```

Then run the program with Python

```sh
$ python structured-data-extraction.py
{
  "sender": "SUNNY FARM",
  "recipient": "Denny Gunawan",
  "address": "221 Queen St\nMelbourne VIC 3000",
  "full_total": "$39.60",
  "subtotal": "$36.00",
  "gst_value": "$3.60",
  "items": [
    {
      "name": "Apple",
      "price_per_kg": "$5.00",
      "quantity_kg": 1
    },
    {
      "name": "Orange",
      "price_per_kg": "$1.99",
      "quantity_kg": 2
    },
    {
      "name": "Watermelon",
      "price_per_kg": "$1.69",
      "quantity_kg": 3
    },
    {
      "name": "Mango",
      "price_per_kg": "$9.56",
      "quantity_kg": 2
    },
    {
      "name": "Peach",
      "price_per_kg": "$2.99",
      "quantity_kg": 1
    }
  ]
}
```



## Further Information

- [Gemini docs link 1](https://ai.google.dev/gemini-api/docs/document-processing)

- [Gemini docs link 2](https://ai.google.dev/gemini-api/docs/structured-output?lang=python)
