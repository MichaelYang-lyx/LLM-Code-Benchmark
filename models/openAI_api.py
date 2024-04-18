import os
import json
import openai
from dotenv import load_dotenv

class OpenAI:
    def __init__(self):
        load_dotenv()
        openai.api_type = "azure"
        openai.base_url = "https://sensebench.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2023-07-01-preview"
        openai.api_version = "2023-07-01-preview"
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate(self, prompt):
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": prompt, 
                }
            ],
        )
        r = response.model_dump_json(indent=4)
        r_dict = json.loads(r)
        return r_dict['choices'][0]['message']['content']


