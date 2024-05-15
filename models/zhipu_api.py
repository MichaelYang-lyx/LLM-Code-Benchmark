import os
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


class Zhipu:
    def __init__(self):
        load_dotenv()
        self.llm = ChatOpenAI(
            temperature=0.95,
            model="glm-4",
            openai_api_key=os.getenv('ZHIPU_API_KEY'),
            openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
        )
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
