# Function calling & tool use

This example demonstrates how to use the Gemini API to call external functions.

Import necessary libraries

```python
import os
from datetime import datetime
from google import genai
from google.genai import types
```

Define the function to get temperature for a location.
In a real application, this would call a weather API service like OpenWeatherMap or WeatherAPI

```python
def get_current_temperature(location: str) -> dict:
    """Gets the current temperature for a given location.

    Note: This is a simplified mock implementation. In a real application,
    this function would make an API call to a weather service provider.
    """
    sample_temperatures = {
        "London": 16,
        "New York": 23,
        "Tokyo": 28,
        "Sydney": 20,
        "Paris": 18,
        "Berlin": 17,
        "Cairo": 32,
        "Moscow": 10,
    }
    temp = sample_temperatures.get(location, 21)
    return {"location": location, "temperature": temp, "unit": "Celsius"}
```

Define the function to check appointment availability.
In a real application, this would query a calendar API like Google Calendar or
a booking system.
For this example, we're using hard-coded busy slots.

```python
def check_appointment_availability(date: str, time: str) -> dict:
    """Checks if there's availability for an appointment at the given date and time."""
    busy_slots = [
        {"date": "2024-07-04", "times": ["14:00", "15:00", "16:00"]},
        {"date": "2024-07-05", "times": ["09:00", "10:00", "11:00"]},
        {"date": "2024-07-10", "times": ["13:00", "14:00"]},
    ]

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {
            "available": False,
            "error": "Invalid date format. Please use YYYY-MM-DD.",
        }

    try:
        datetime.strptime(time, "%H:%M")
    except ValueError:
        return {
            "available": False,
            "error": "Invalid time format. Please use HH:MM in 24-hour format.",
        }

    for slot in busy_slots:
        if slot["date"] == date and time in slot["times"]:
            return {
                "available": False,
                "message": f"The slot on {date} at {time} is already booked.",
            }

    return {
        "available": True,
        "message": f"The slot on {date} at {time} is available for booking.",
    }
```

For Example 1, we will call a single function with Gemini.

```python
print("\n--- Example 1: Basic Function Calling ---\n")
```

First, we define the function declaration that will be provided to the model.

```python
weather_function = {
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. San Francisco",
            },
        },
        "required": ["location"],
    },
}
```

Create a client and configure it with the function declaration

```python
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
tools = types.Tool(function_declarations=[weather_function])
config = types.GenerateContentConfig(tools=[tools])
```

Send a request to Gemini that will likely trigger the function

```python
response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents="What's the temperature in London?",
    config=config,
)
```

Check if Gemini responded with a function call
Assumes Gemini will always respond with a function call.

```python
function_call = response.candidates[0].content.parts[0].function_call
print(f"Function to call: {function_call.name}")
print(f"Arguments: {function_call.args}")
```

Execute the function with the arguments Gemini provided

```python
result = get_current_temperature(**function_call.args)
print(f"Function result: {result}")
```

Send the function result back to Gemini for a final response

```python
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        {
            "parts": [
                {
                    "function_response": {
                        "name": function_call.name,
                        "response": result,
                    }
                }
            ]
        }
    ],
)
print(f"Model's final response: {response.text}")
```

Example 2 shows how to use multiple functions simultaneously.

```python
print("\n--- Example 2: Parallel Function Calling (Weather and Appointments) ---\n")
```

Define the weather function declaration

```python
weather_function = {
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. London",
            },
        },
        "required": ["location"],
    },
}
```

Define the appointment function declaration

```python
appointment_function = {
    "name": "check_appointment_availability",
    "description": "Checks if there's availability for an appointment at the given date and time.",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "Date to check (YYYY-MM-DD)",
            },
            "time": {
                "type": "string",
                "description": "Time to check (HH:MM) in 24-hour format",
            },
        },
        "required": ["date", "time"],
    },
}
```

Create a client and configure it with both function declarations

```python
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
tools = [types.Tool(function_declarations=[weather_function, appointment_function])]
```

Set a lower temperature for more predictable function calling

```python
config = {
    "tools": tools,
    "temperature": 0.1,
}
```

Start a chat and send a message that should trigger both functions

```python
chat = client.chats.create(model="gemini-2.0-flash-lite", config=config)
response = chat.send_message(
    "I'm planning to visit Paris on July 4th at 2 PM. What's the weather like there and is that slot available for an appointment?"
)
```

Store the results from each function call

```python
results = {}
```

Process each function call Gemini requests
Assumes Gemini will always respond with function calls.

```python
for fn in response.function_calls:
    args_str = ", ".join(f"{key}={val}" for key, val in fn.args.items())
    print(f"{fn.name}({args_str})")
```

Call the appropriate function based on name

```python
if fn.name == "get_current_temperature":
        result = get_current_temperature(**fn.args)
    elif fn.name == "check_appointment_availability":
        result = check_appointment_availability(**fn.args)
    else:
        result = {"error": f"Unknown function: {fn.name}"}
```

Store each result for later use

```python
results[fn.name] = result
    print(f"Result: {result}\n")
```

Prepare all function responses to send back to Gemini

```python
function_responses = []
for fn_name, result in results.items():
    function_responses.append({"name": fn_name, "response": result})
```

Send all results back to Gemini in a single message

```python
if function_responses:
    print("Sending all function results back to the model...\n")
    response = chat.send_message(str(function_responses))
    print(f"Model's final response:\n{response.text}")
```



## Running the Example

First, install the Google Generative AI library and requests

```sh
$ pip install google-genai requests

```

Then run the program with Python

```sh
$ python function_calling_weather_calendar.py
--- Example 1: Basic Function Calling ---
Function to call: get_current_temperature
Arguments: {'location': 'London'}
Function result: {'location': 'London', 'temperature': 16, 'unit': 'Celsius'}
Model's final response: OK. The current temperature in London is 16 degrees Celsius.
--- Example 2: Parallel Function Calling (Weather and Appointments) ---
get_current_temperature(location=Paris)
Result: {'location': 'Paris', 'temperature': 18, 'unit': 'Celsius'}
check_appointment_availability(time=14:00, date=2024-07-04)
Result: {'available': False, 'message': 'The slot on 2024-07-04 at 14:00 is already booked.'}
Sending all function results back to the model...
Model's final response:
The current temperature in Paris is 18 degrees Celsius. The appointment slot on July 4th at 2 PM is not available.
```



## Further Information

- [Gemini docs link 1](https://ai.google.dev/gemini-api/docs/function-calling?example=weather)

- [Gemini docs link 2](https://ai.google.dev/gemini-api/docs/function-calling?example=meeting)
