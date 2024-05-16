import os
import json
import openai
from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
class OpenAI:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        os.environ["OPENAI_API_BASE"] = 'https://gtapi.xiaoerchaoren.com:8932/v1'
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_PROXY_KEY")
        
        self.llm = ChatOpenAI()
        self.prompt_template = PromptTemplate(
            input_variables=["prompt"],
            template="User's input: {prompt}"
        )

    def generate(self, prompt):
        formatted_prompt = self.prompt_template.format(prompt=prompt)
        response = self.llm.invoke(
            formatted_prompt
        )
        # Assuming response is a list of LLMResult objects, get the first generation's content
        message_content = response.content
        return message_content
