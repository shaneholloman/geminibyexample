# Translate documents

This example demonstrates how to load content from a URL and translate it into
Chinese using the Gemini API.
It's easy to do the same using PDF or Markdown files, though you might want to
split it up into smaller chunks for better accuracy if your document is long.

Import the necessary libraries

```python
from google import genai
import requests
import os
```

Initialize the Gemini client with your API key

```python
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```

Define the URL of the content to be translated

```python
url = "https://raw.githubusercontent.com/zenml-io/zenml/refs/heads/main/README.md"
```

Fetch the content from the URL

```python
response = requests.get(url)
text_content = response.text
```

Define the prompt for translation

```python
prompt = f"Translate the following English text to Chinese: {text_content}"
```

Generate the translated content using the Gemini API.
We're using the 2.0-flash-lite model here for speed, but you probably would
want to use a more powerful model for better results.

```python
model = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents=prompt,
)
```

Print the translated text

```python
print(model.text)
```



## Running the Example

First, install the Google Generative AI library and requests

```sh
$ pip install google-genai requests

```

Then run the program with Python

```sh
$ python translate.py
```chinese
<div align="center">
  <img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=0fcbab94-8fbe-4a38-93e8-c2348450a42e" />
  <h1 align="center">超越演示：生产级 AI 系统</h1>
  <h3 align="center">ZenML 将经过实战检验的 MLOps 实践带入您的 AI 应用，处理大规模的评估、监控和部署</h3>
</div>
<!-- 项目徽章 -->
<!--
*** 我使用 Markdown "引用样式" 链接以提高可读性。
*** 引用链接用方括号 [ ] 括起来，而不是用括号 ( )。
*** 请参阅本文档底部，了解贡献者网址、分支网址等的引用变量声明。 这是一个可选的、简洁的语法，您可以使用它。
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<div align="center">
  <!-- 项目 Logo -->
  <br />
    <a href="https://zenml.io">
      <img alt="ZenML Logo" src="docs/book/.gitbook/assets/header.png" alt="ZenML Logo">
    </a>
  <br />
etc...
```



## Further Information

- [Gemini docs link 1](https://ai.google.dev/gemini-api/docs/document-processing?lang=python)

- [Gemini docs link 2](https://ai.google.dev/gemini-api/docs/document-processing?lang=rest)
