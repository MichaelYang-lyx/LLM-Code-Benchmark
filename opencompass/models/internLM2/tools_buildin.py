import requests
import json
import base64
import time
import re


code_agent_define = {
        "function": {
            "description": "This function serves as a code agent. It will analyze the query, execute it, and give the final answer",
            "name": "code_agent",
            "parameters": {
                "properties": {
                    "prompt": {
                        "description": "A detailed textual description used to accomplish the task. The prompt should be clear and descriptive, containes all the information needed to produce the desired result. need execute. While the primary language for prompt is Chinese, prompt in other languages are also accepted and processed. do not generate code directly!!!",
                        "type": "string"
                    }
                },
            "required": [
                "prompt"
            ],
            "type": "object"
            }
        },
        "type": "function"
    }

text2image_define = {
            "type": "function",
            "function": {
                "name": "text2image",
                "description": "This function generates a visual representation of a given textual description. It is capable of creating images in various styles based on the provided prompts, adhering to specified guidelines and constraints for content.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "A detailed textual description used to generate the image. The prompt should be clear and descriptive, potentially including details about the desired style, color scheme, and content of the image. There may be limitations on the length and complexity of the description."
                        }
                    },
                    "required": ["prompt"]
                }               
            }
        }

vqa_agent_define =  {
            "type": "function",
            "function": {
                "name": "vqa_agent",
                "description": "This function serves as a Visual Question Answering agent, adept at comprehending image-based queries and providing corresponding responses.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "A refined question, derived from the original question and conversation histories. The agent utilizes this prompt to answer questions about the provided image."
                        },
                        "image": {
                            "type": "string",
                            "description": "The URL of an image from conversation histories that this question refers to."
                        }
                    },
                    "required": ["prompt", "image"]
                }
            }
        }

web_search_define = {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "This function acts as a search engine to retrieve a wide range of information from the web. It is capable of processing queries related to various topics and returning relevant results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query used to retrieve information from the internet. While the primary language for queries is Chinese, queries in other languages are also accepted and processed."
                        }
                    },
                    "required": ["query"]
                }                
            }
        }

data_analysis_define = {
            "type": "function",
            "function": {
                "name": "data_analysis",
                "description": "This function acts as a Data Analysis Tool for automatically analyzing uploaded files or provided data",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "A refined question and provided data for data analysis tool"
                        },
                        "file": {
                            "type": "string",
                            "description": "The URL of file"
                        }
                    },
                    "required": ["prompt", "file"]
                  }
            }
        }

python_interpreter_define = {
            "type": "function",
            "function": {
                "name": "python_interpreter",
                "description": "This function serves as a Python interpreter, executing provided Python code within certain constraints.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The Python code to be executed."
                        }
                    },
                    "required": ["code"]
                }               
            }
    }


tools_define_buildin = [web_search_define, code_agent_define, text2image_define, vqa_agent_define]
tools_define_buildin_0131 = [web_search_define, data_analysis_define, text2image_define, vqa_agent_define, python_interpreter_define]
tools_define_buildin_0131_no_interpreter = [web_search_define, data_analysis_define, text2image_define, vqa_agent_define]


description = """你现在可以使用一个支持 Python 代码执行的 Jupyter 笔记本环境。只需向 python 发送代码，即可在这个有状态环境中进行运行。这功能适用于:
- 数据分析或处理（如数据操作和图形制作）
- 复杂计算（如数学和物理问题）
- 编程示例（用于理解编程概念或语言特性）
- 文本处理和分析（包括文本分析和自然语言处理）
- 机器学习和数据科学（模型训练和数据可视化展示）
- 文件操作和数据导入（处理CSV、JSON等格式文件）"""

interpreter = [{"name": "python_interpreter", "description": description}]


def web_search(query, top_k=1):
    sogou_server = "http://10.112.97.25:32015"
    url = "{}/search".format(sogou_server)

    data = {
                "query": query,
                "engine": "SOGOU_FULL",
    }

    headers = {
                "Content-type": "application/json"
            }

    rsp = requests.post(url, data=json.dumps(data), headers=headers)
    out = json.loads(rsp.text)


    answer = out['ans_dic']['ans_str']
    if answer:
        web_contents = [answer]
        return web_contents[0]

    web_contents = []
    results = out['all_snip_dics']
    if results:
        results = results[:top_k]
        for result in results:
            if result['passage']:
                web_contents.append(result['passage'])
            else:
                web_contents.append(result['snippet'])
    return web_contents[0]


def code_agent(prompt):
    url = "http://10.4.236.13:15984/"
    history = []
    history.append({
             "role": "user",
             "content": prompt
    })
    payload = {
            "messages": history,
            "parameters": {"yield_messages": False, 'image_to_data_url_markdown': True}
        }
    r = requests.post(url, json=payload, proxies={'https': ''})
    rsp = r.json()
    
    answer = ""
    for msg in rsp['new_messages']:
        role = msg['role']
        if role == 'code':
            answer += msg['code']
        elif role == 'assistant':
            answer += msg['content']

    return answer


def text2image(prompt):
    api_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyWlFhZFVRQ1J2SGJQN3hLTHJRNVBTQmJWangiLCJleHAiOjE3MDU5NjY1MDMsIm5iZiI6MTcwNDE2NjQ5OH0.OmFGMmePOmp_HxeROL1HzRfFGSxYCWPddLp4fPUhIws'
    mirage_url = 'https://api.stage.sensenova.cn/v1/imgen/internal/generation_tasks'
    mirage_models_url = 'https://api.stage.sensenova.cn/v1/imgen/models'
    headers = {
            "Authorization": f'Bearer {api_token}',
            "Content-Type": "application/json"
        }
    
    payload = {
            "prompt": prompt,
            "model_id": "sgl_artist_v0.3.5_0925",
        }
    r = requests.post(mirage_url, json=payload, headers=headers, proxies={'https': ''})
    rsp = r.json()
    task_id = rsp['task_id']
    
    def get_img(task_id):
        url = f'{mirage_url}/{task_id}'
        r = requests.get(url, headers=headers, proxies={'https': ''})
        rsp = r.json()
        task = rsp['task']
        state = task['state']
        if state == 'SUCCESS':
            img_url = task['result'][0]['raw']
        else:
            img_url = ''
        return img_url

    def get_img_wait(task_id):
        img_url = get_img(task_id)
        while img_url == '':
            print('waiting img generating...')
            import time
            time.sleep(1)
            img_url = get_img(task_id)
        return img_url
    
    return get_img_wait(task_id)


def vqa_agent(image, prompt):
    url = "https://api.sensenova.cn/v1/llm/internal/multi-chat"
    ak = '2ZnO3279j01wbmtvpcZhZ8MDn72'
    sk = 'lnHLPX766a1tVhDBYKsYp78qAn6875gF'

    history = []
    history.append({
            "role": "user",
            "content": prompt
    })

    def get_image(url_or_image):
        if url_or_image.startswith("http://") or url_or_image.startswith("https://"):
            response = requests.get(url_or_image)
            if response.status_code == 200:
                # Encode the image content to base64
                base64_image = base64.b64encode(response.content).decode('utf-8')
                return base64_image
            else:
                print(f"Failed to download image. Status code: {response.status_code}")
                return None
        else:
            return url_or_image

    image_base64 = get_image(image)
    if image_base64 is None:
        return f"{image}: 图片地址无效"

    payload = {
            "messages": history,
            "image": image_base64,
            "temperature": 0.5,
            "top_p": 0.7,
            "max_new_tokens": 1024,
            "repetition_penalty": 1.05,
            "model": "nova-pli-s-v1-1"
        }
    
    def get_headers():
        import jwt
        
        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }
        payload = {
            "iss": ak,
            "exp": int(time.time()) + 1800,  # 有效时间
            "nbf": int(time.time()) - 5  # 签发时间
        }
        token = jwt.encode(payload, sk, headers=headers)
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    r = requests.post(url, json=payload, headers=get_headers(), proxies={'https': ''})
    rsp = r.json()
    if 'error' in rsp:
        return rsp['error']['message']
    return rsp['data']['choices'][0]['message']


def extract_python_code(markdown_text):
    # 使用正则表达式提取Python代码块
    code_blocks = re.findall(r'```python\n(.*?)\n```', markdown_text, re.DOTALL)

    # 将提取的代码块保存到Python脚本中
    python_script = '\n\n'.join(code_blocks)

    return python_script


def python_interpreter_func(code_markdown):
    from pumpcoder_sandbox_client import RunCKernelClient
    
    code = extract_python_code(code_markdown)
    
    py_client = RunCKernelClient(
        host='pumpcoder.mtc.sensetime.com',
        port=80,
        base_uri='/sandbox',
        token='OGY4ZmM1Y2MtNjQ0ZC00ODIxLWE0MmItMjRmOWZkYzliMGYy',
        msg_timeout=60.0,
    )
    
    res = py_client.execute_code_blocking(code)
    py_client.close()
    
    # check result
    res_return = {}
    if res.result:
        res_return['data_obj'] = res.result.data_obj
    if res.error:
        res_return['error'] = res.error
    return res_return