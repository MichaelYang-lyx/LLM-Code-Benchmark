#Note: The openai-python library support for Azure OpenAI is in preview.

import os
import json
import openai
from dotenv import load_dotenv
load_dotenv()


openai.api_type = "azure"
openai.base_url = "https://sensebench.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2023-07-01-preview"
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

message_text = [{"role":"system","content":"You are an AI assistant that helps people find information."}]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    }
]

response = openai.chat.completions.create(
  model="gpt-4",
  messages=[
      {
          "role": "user",
          "content": "今天深圳天气怎么样", 
      }
  ],
)

r = response.model_dump_json(indent=4)
r_dict = json.loads(r)
print(r_dict)
print(r_dict['choices'][0]['message']['content'])
