# Model Context Protocol

This example demonstrates using a local MCP server with Gemini to get weather information.

Import necessary libraries. Make you have mcp installed.

```python
import asyncio
import os
from datetime import datetime
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
```

Configure Gemini client

```python
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```

Define server parameters for the MCP server

```python
server_params = StdioServerParameters(
    command="npx",  # Executable for the MCP server
    args=[
        "-y",
        "@philschmid/weather-mcp",
    ],  # Arguments for the server (Weather MCP Server)
    env=None,  # Optional environment variables
)
```

Define the prompt to get the weather for the current day in Delft

```python
PROMPT = f"What is the weather in Delft in {datetime.now().strftime('%Y-%m-%d')}?"
```

Define an asynchronous function to run the MCP client and interact with
Gemini.
We retrieve tools from the MCP session and convert them to Gemini Tool objects

```python
async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            mcp_tools = await session.list_tools()
            tools = [
                types.Tool(
                    function_declarations=[
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": {
                                k: v
                                for k, v in tool.inputSchema.items()
                                if k not in ["additionalProperties", "$schema"]
                            },
                        }
                    ]
                )
                for tool in mcp_tools.tools
            ]

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=PROMPT,
                config=types.GenerateContentConfig(
                    temperature=0,
                    tools=tools,
                ),
            )

            if response.candidates[0].content.parts[0].function_call:
                function_call = response.candidates[0].content.parts[0].function_call
                print(f"Function call: {function_call}")

                result = await session.call_tool(
                    function_call.name, arguments=function_call.args
                )
                print(f"Tool Result: {result.content[0].text}")

            else:
                print("No function call found in the response.")
                print(response.text)
```

Run the asynchronous function

```python
asyncio.run(run())
```



## Running the Example

First, install the necessary libraries

```sh
$ pip install google-genai mcp

```

Then run the program with Python

```sh
$ python mcp_example.py
Function call: id=None args={'date': '2025-04-05', 'location': 'Delft'} name='get_weather_forecast'
Tool Result: {"2025-04-05T00:00":11.4,"2025-04-05T01:00":10.3,"2025-04-05T02:00":9.8,"2025-04-05T03:00":9.1,"2025-04-05T04:00":8,"2025-04-05T05:00":8,"2025-04-05T06:00":8.3,"2025-04-05T07:00":9.1,"2025-04-05T08:00":11.1,"2025-04-05T09:00":12.8,"2025-04-05T10:00":14.3,"2025-04-05T11:00":15.6,"2025-04-05T12:00":16,"2025-04-05T13:00":16.4,"2025-04-05T14:00":17,"2025-04-05T15:00":16.6,"2025-04-05T16:00":16.1,"2025-04-05T17:00":15,"2025-04-05T18:00":13.5,"2025-04-05T19:00":11.9,"2025-04-05T20:00":11.1,"2025-04-05T21:00":10.7,"2025-04-05T22:00":10.1,"2025-04-05T23:00":9.3}
```



## Further Information

- [Gemini docs link 1](https://ai.google.dev/gemini-api/docs/function-calling?example=weather#use_model_context_protocol_mcp)
