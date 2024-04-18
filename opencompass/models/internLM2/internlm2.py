import json
from typing import List
import requests
import time
from datetime import datetime
from typing import Dict, List, Optional

from opencompass.models.base_api import PromptType
from ..base_api import BaseAPIModel
from concurrent.futures import ThreadPoolExecutor
from .tools_buildin import tools_define_buildin_0131_no_interpreter
from .general import sys_prompt_v2 



CONVSATION_START = "<|im_start|>"
CONVSATION_END = "<|im_end|>"
PLUGIN_START = "<|action_start|>"
PLUGIN_END = "<|action_end|>"
CODE_INTERPRETER = "<|interpreter|>"
TOOLS_DEFINE = "<|plugin|>"



default_parameters_Gauss_20B = {
    'temperature': 1.0,
    'top_p': 0.8,
    'top_k': 40,
    'repetition_penalty': 1.02,
    'max_new_tokens': 512,
    'do_sample': False
}

description = """你现在可以使用一个支持 Python 代码执行的 Jupyter 笔记本环境。只需向 python 发送代码，即可在这个有状态环境中进行运行。这功能适用于:
- 数据分析或处理（如数据操作和图形制作）
- 复杂计算（如数学和物理问题）
- 编程示例（用于理解编程概念或语言特性）
- 文本处理和分析（包括文本分析和自然语言处理）
- 机器学习和数据科学（模型训练和数据可视化展示）
- 文件操作和数据导入（处理CSV、JSON等格式文件）"""

interpreter = [{"name": "python_interpreter", "description": description}]


class Internlm2(BaseAPIModel):
    def __init__(self, 
                 path: str = '', 
                 url: str = '', 
                 key: str = '', 
                 tools=[],
                 system_info="", 
                 max_seq_len=4096, 
                 query_per_second = 1, 
                 meta_template=None, 
                 retry: int = 3, 
                 generation_kwargs: Optional[Dict] = dict()):
        super().__init__(path=path,
                         max_seq_len=max_seq_len,
                         query_per_second=query_per_second,
                         meta_template=meta_template)
        
        self.url = url
        self.key = key
        self.headers = {'Content-Type': 'application/json'}
        if self.key:
            self.headers['Authorization'] = f'Bearer {key}'
        self.parameters = default_parameters_Gauss_20B
        self.model = path
        self.retry = retry
        self.generation_kwargs = generation_kwargs
        # self.pure_tools = pure_tools

        self.tools = tools
        self.system_info = system_info


    def parse_intern_function(self, response):
        interpreter_left = response.find(f"{CODE_INTERPRETER}")
        tool_left = response.find(f"{TOOLS_DEFINE}")
        right = response.find(f"{PLUGIN_END}")

        reses = []
        if ((interpreter_left == -1) and (tool_left == -1)) or right == -1 or ((interpreter_left != -1) and (tool_left != -1)):
            return response

        if (interpreter_left == -1):
            left = tool_left
        else:
            left = interpreter_left
        
        if left >= right:
            return response

        if (interpreter_left == -1):
            tool_str = response[left + len(TOOLS_DEFINE):right]
            calls = tool_str.split(TOOLS_DEFINE)
            for call in calls:
                call = call.strip()
                try:
                    call = json.loads(call)
                    if "parameters" in call:
                        call["arguments"] = call["parameters"]
                    reses.append(call)
                except:
                    pass
            if len(reses) == 0:
                return response
        else:
            calls = response[left+len(CODE_INTERPRETER):right]
            calls = calls.strip()
            try:
                assert (calls.strip()[:10] == "```python\n") and (calls.strip()[-4:] == "\n```")
                code_calls = {'name': 'python_interpreter', 'arguments': {'code': calls}}
                reses.append(code_calls)
            except:
                return response
        return reses    
    
    def chat(self, query, interpreter=[]):
        system_info = self.system_info.replace("<system>: ", "")
        system_text = f"{CONVSATION_START}system\n{system_info}{CONVSATION_END}\n"
        if interpreter:
            assert (len(interpreter) == 1) and (interpreter[0]["name"] == "python_interpreter"), "Only support python interpreter now!"     # noqa
            interpreter_test = f"{CONVSATION_START}system name={CODE_INTERPRETER}\n{interpreter[0]['description']}\n{CONVSATION_END}\n"
        else:
            interpreter_test = ""

        pure_tools = []
        for tool in self.tools:
            if tool['function']['name'] != "python_interpreter":
                pure_tools.append(tool['function'])
        
        if pure_tools:
            tool_text_str = json.dumps(pure_tools, ensure_ascii=False)
            tool_text = f"{CONVSATION_START}system name={TOOLS_DEFINE}\n{tool_text_str}\n{CONVSATION_END}\n"
        else:
            tool_text = ""
        conv_text = f"{CONVSATION_START}user\n{query}{CONVSATION_END}\n"
        input_text = system_text + interpreter_test + tool_text + conv_text + f"{CONVSATION_START}assistant\n"
    

        input_data = {
            "inputs": input_text,
            "parameters": self.parameters
        }

        num_try = 0

        while num_try < 5:
            # call function
            response = requests.post(self.url, headers=self.headers, json=input_data, stream=True)
            if response.status_code == 200:
                response = response.json()
                try:
                    response = response['generated_text'][0]
                except:
                    response = response[0]['generated_text']

                res = self.parse_intern_function(response)

                try:
                    res = res.split(CONVSATION_END)[0]
                except:
                    pass
                
                return res  
            
            else:
                self.logger.warning(f'error status code: {response.status_code}')
                time.sleep(1)
                num_try += 1
                continue

        raise RuntimeError(f'request id: {response.headers.get("X-Request-Id")}, code: {response.status_code} , {response.text}')

    def generate(self, inputs, max_out_len=512):
        with ThreadPoolExecutor() as executor:
            results = list(
                executor.map(self.chat, inputs))
        self.flush()
        return results

if __name__ == "__main__":
    query = "Melanie是一个挨家挨户的推销员。她把三分之一的吸尘器卖给了绿房子，又把两个卖给了红房子，剩下的一半卖给了橙房子。如果梅兰妮还剩下5台吸尘器，她一开始有多少台？"
    model = Internlm2()
    res  = model.chat(query)
    print(res)

    
    