# PDF and CSV data analysis and summarization

This example demonstrates how to use the Gemini API to analyze data from PDF and CSV files.

Import necessary libraries

```python
from google import genai
from google.genai import types
import httpx
import os
```

Initialize the Gemini client with your API key

```python
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```

We start with the PDF analysis.
Download the PDF file

```python
pdf_url = "https://www.princexml.com/samples/invoice/invoicesample.pdf"
pdf_data = httpx.get(pdf_url).content
```

Prompt to extract main players from the PDF

```python
pdf_prompt = (
    "Identify the main companies or entities mentioned in this invoice. "
    "Summarize the data."
)
```

Generate content with the PDF and the prompt

```python
pdf_response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        types.Part.from_bytes(data=pdf_data, mime_type="application/pdf"),
        pdf_prompt,
    ],
)
```

Print the PDF analysis result

```python
print("PDF Analysis Result:\n", pdf_response.text)
```

Moving on to the CSV analysis now. You'll note that the process is very
similar.
You can also pass in code files, XML, RTF, Markdown, and more.
We download the CSV file here.

```python
csv_url = "https://gist.githubusercontent.com/suellenstringer-hye/f2231b3383538bcb1a5b051c7908f5b7/raw/0f4e0733a434733cda8e749bbbf33a93c2b5bbde/test.csv"
csv_data = httpx.get(csv_url).content
```

Prompt to analyze the CSV data

```python
csv_prompt = "Analyze this data and tell me about the contents. Summarize the data."
```

Generate content with the CSV data and the prompt

```python
csv_response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        types.Part.from_bytes(
            data=csv_data,
            mime_type="text/csv",
        ),
        csv_prompt,
    ],
)
```

Print the CSV analysis result

```python
print("\nCSV Analysis Result:\n", csv_response.text)
```



## Running the Example

First, install the Google Generative AI library and httpx (for downloading files)

```sh
$ pip install google-genai httpx pandas

```

Then run the program with Python

```sh
$ python pdf_csv_analysis.py
PDF Analysis Result:
 The main company mentioned in the invoice is Sunny Farm.
CSV Analysis Result:
 Okay, I've analyzed the provided data. Here's a summary of its contents:
**Data Format:**
*   The data appears to be in CSV (Comma Separated Values) format.
*   The first line is a header row defining the fields.
*   Each subsequent line represents a record containing information about a person.
**Fields Present:**
The data includes the following fields for each person:
1.  **first\_name:** The person's first name.
2.  **last\_name:** The person's last name.
3.  **company\_name:** The name of the company they are associated with.
4.  **address:** The street address.
5.  **city:** The city.
6.  **county:** The county.
7.  **state:** The state.
8.  **zip:** The zip code.
9.  **phone1:** The primary phone number.
10. **phone2:** A secondary phone number.
11. **email:** The email address.
12. **web:** The website address (presumably for the associated company).
```



## Further Information

- [Gemini docs link 1](https://ai.google.dev/gemini-api/docs/document-processing?lang=python)

- [Gemini docs link 2](https://ai.google.dev/gemini-api/docs/document-processing?lang=rest)
