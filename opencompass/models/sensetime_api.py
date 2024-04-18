import json
import os
import time
import requests
import json
import shutil
import mmengine

from io import BytesIO
from typing import Dict, List, Optional, Union
from datetime import datetime
from .base_api import BaseAPIModel


from concurrent.futures import ThreadPoolExecutor
from opencompass.utils.prompt import PromptList

PromptType = Union[PromptList, str]


class SenseTime(BaseAPIModel):
    """Model wrapper around SenseTime.

    Args:
        path (str): The name of SenseTime model.
            e.g. `nova-ptc-xl-v1`
        key (str): Authorization key.
        query_per_second (int): The maximum queries allowed per second
            between two consecutive calls of the API. Defaults to 1.
        max_seq_len (int): Unused here.
        meta_template (Dict, optional): The model's meta prompt
            template if needed, in case the requirement of injecting or
            wrapping of any meta instructions.
        retry (int): Number of retires if the API call fails. Defaults to 2.
    """

    def __init__(
        self,
        path: str,
        url: str,
        tools = [],
        key: str = 'ENV',
        query_per_second: int = 2,
        max_seq_len: int = 2048,
        meta_template: Optional[Dict] = None,
        retry: int = 2,
        parameters: Optional[Dict] = None,
    ):
        super().__init__(path=path,
                         max_seq_len=max_seq_len,
                         query_per_second=query_per_second,
                         meta_template=meta_template,
                         retry=retry)
        
        if isinstance(key, str):
            self.keys = os.getenv('SENSENOVA_API_KEY') if key == 'ENV' else key
        else:
            self.keys = key

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.keys}'
        }
        self.url = url
        self.model = path
        self.params = parameters
        self.tools = tools

    def generate(
        self,
        inputs: List[str or PromptList],
        max_out_len: int = 512,
    ) -> List[str]:
        """Generate results given a list of inputs.

        Args:
            inputs (List[str or PromptList]): A list of strings or PromptDicts.
                The PromptDict should be organized in OpenCompass'
                API format.
            max_out_len (int): The maximum length of the output.

        Returns:
            List[str]: A list of generated strings.
        """
        with ThreadPoolExecutor() as executor:
            results = list(
                executor.map(self._generate, inputs,
                             [max_out_len] * len(inputs)))
        self.flush()
        return results

    def _generate(
        self,
        input: str or PromptList,
        max_out_len: int = 512,
    ) -> str:
        """Generate results given an input.

        Args:
            inputs (str or PromptList): A string or PromptDict.
                The PromptDict should be organized in OpenCompass'
                API format.
            max_out_len (int): The maximum length of the output.

        Returns:
            str: The generated string.
        """
        assert isinstance(input, (str, PromptList))

        if isinstance(input, str):
            messages = [{'role': 'user', 'content': input}]
        else:
            messages = []
            for item in input:
                msg = {'content': item['prompt']}
                if item['role'] == 'HUMAN' or item['role'] == 'user':
                    msg['role'] = 'user'
                elif item['role'] == 'BOT' or item['role'] == 'assistant':
                    msg['role'] = 'assistant'

                messages.append(msg)

        data = {'messages': messages, 'model': self.model}
        data.update(self.params)

        if self.tools:
            data.update({
                "tools": self.tools,
                "tool_choice": {
                    "mode": "auto"
                }
            })

        stream = data['stream']

        max_num_retries = 0
        while max_num_retries < self.retry:
            self.acquire()

            max_num_retries += 1
            raw_response = requests.request('POST',
                                            url=self.url,
                                            headers=self.headers,
                                            json=data)
            requests_id = raw_response.headers["X-Request-Id"]
            self.release()


            if not stream:
                response = raw_response.json()

                if response is None:
                    print('Connection error, reconnect.')
                    # if connect error, frequent requests will casuse
                    # continuous unstable network, therefore wait here
                    # to slow down the request
                    self.wait()
                    continue
                if raw_response.status_code == 200:
                    if not self.tools:
                        msg = response['data']['choices'][0]['message']
                        return msg
                    else:
                        finish_reason = response['data']['choices'][0]['finish_reason']
                        if finish_reason == 'stop':
                            return response['data']['choices'][0]['message']
                        elif finish_reason == 'tool_calls':
                            return response['data']['choices'][0]['tool_calls'][0]['function']['name']
                        else:
                            return str(raw_response.text)

                if (raw_response.status_code != 200):
                    if response['error']['code'] == 18:
                        # security issue
                        return 'error:unsafe'
                    if response['error']['code'] == 17:
                        return 'error:too long'
                    else:
                        print(raw_response.text)
                        time.sleep(1)
                        continue
            else:
                # stream data to msg
                raw_response.encoding = 'utf-8'

                if raw_response.status_code == 200:
                    response_text = raw_response.text
                    data_blocks = response_text.split("data:")
                    data_blocks = data_blocks[1:]

                    first_block = json.loads(data_blocks[0])
                    if first_block['status']['code'] != 0:
                        msg = f"error:{first_block['status']['code']}, {first_block['status']['message']}"
                        self.logger.error(msg)
                        return msg

                    msg = ""
                    for i, part in enumerate(data_blocks):
                        # print(f'process {i}: {part}')
                        try:
                            if part.startswith('[DONE]'):
                                break

                            json_data = json.loads(part)
                            choices = json_data["data"]["choices"]
                            for c in choices:
                                delta=c.get("delta")
                                msg += delta
                        except json.decoder.JSONDecodeError as e:
                            self.logger.error(f"Error decoding JSON: {part}")
                    return msg

                else:
                    print(raw_response.text, raw_response.headers.get('X-Request-Id'))
                    time.sleep(1)
                    continue


        raise RuntimeError(f'request id: {raw_response.headers.get("X-Request-Id")}, {raw_response.text}')

class SenseTimeAssistant(BaseAPIModel):
    """Model wrapper around SenseTime.

    Args:
        path (str): The name of SenseTime model.
            e.g. `nova-ptc-xl-v1`
        key (str): Authorization key.
        query_per_second (int): The maximum queries allowed per second
            between two consecutive calls of the API. Defaults to 1.
        max_seq_len (int): Unused here.
        meta_template (Dict, optional): The model's meta prompt
            template if needed, in case the requirement of injecting or
            wrapping of any meta instructions.
        retry (int): Number of retires if the API call fails. Defaults to 2.
    """

    def __init__(
        self,
        path: str,
        url: str,
        key: str = 'ENV',
        query_per_second: int = 2,
        max_seq_len: int = 2048,
        meta_template: Optional[Dict] = None,
        retry: int = 2,
        parameters: Optional[Dict] = None,
    ):
        super().__init__(path=path,
                         max_seq_len=max_seq_len,
                         query_per_second=query_per_second,
                         meta_template=meta_template,
                         retry=retry)
        if isinstance(key, str):
            self.keys = os.getenv('SENSENOVA_API_KEY') if key == 'ENV' else key
        else:
            self.keys = key

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.keys}'
        }
        self.url = url
        self.model = path
        self.params = parameters

        self.picture_cache_dir = f'tmp/{self.model}'
        self.logger.info(f'picture_cache_dir: {self.picture_cache_dir}')
        mmengine.mkdir_or_exist(self.picture_cache_dir)

    def generate(
        self,
        inputs: List[str or PromptList],
        max_out_len: int = 512,
    ) -> List[str]:
        """Generate results given a list of inputs.

        Args:
            inputs (List[str or PromptList]): A list of strings or PromptDicts.
                The PromptDict should be organized in OpenCompass'
                API format.
            max_out_len (int): The maximum length of the output.

        Returns:
            List[str]: A list of generated strings.
        """
        with ThreadPoolExecutor() as executor:
            results = list(
                executor.map(self._generate, inputs,
                             [max_out_len] * len(inputs)))
        self.flush()
        return results

    def create_assistant(self):
        body = {
            "name": "assistant_1", 
            "model": f"{self.model}",
            "tools": [{"type": "web_search"}, {"type": "text2image"}, {"type": "vqa_agent"}, {"type": "data_analysis"}],
            "instructions": "你是SenseChat，一个由商汤科技开发的人工智能助手，可以利用各种工具来辅助解答各种问题。你可以同时调用多个工具，也可以顺序调用工具，遇到图片链接可以当做真实的图片，图片链接应该包含所有的参数，你的答复应尽量使用中文。请尽量优化你的回答，确保信息的准确性和有用性以及简洁性。不依赖工具的问题可以直接回答。如果工具的最新回答有图片链接，你需要用markdown格式展示出来。当用户上传数据或者表格文件时，你需要调用data_analysis数据分析工具来回答。针对图片的问题你需要从历史对话中提取正确的图片链接，调用vqa_agent来回答。"
        }
        resp = requests.post(self.url+"/v1/assistants", json=body, headers=self.headers)
        assistant_id = resp.json().get("id")
        return assistant_id

    def create_thread(self):
        body = {}
        resp = requests.post(self.url+"/v1/threads", json=body, headers=self.headers)
        thread_id = resp.json().get("id")
        return thread_id

    def create_message(self, thread_id, messages):
        resp = requests.post(self.url+"/v1/threads/"+thread_id+"/messages", json=messages, headers=self.headers)        
        return resp

    def create_run(self, assistant_id, thread_id):
        body = {
            "assistant_id": assistant_id,
        }
        resp = requests.post(self.url+"/v1/threads/"+thread_id+"/runs", json=body, headers=self.headers)

        return resp

    def get_run_status(self, thread_id, run_id):
        resp = requests.get(self.url+"/v1/threads/"+thread_id+"/runs/"+run_id, headers=self.headers)
        return resp.json().get("run", {}).get("result", {}).get("status", "")

    def list_msgs_by_thread_id(self, thread_id):
        resp = requests.get(self.url+"/v1/threads/"+thread_id+"/messages", headers=self.headers)
        return resp.json()

    def get_file_url(self, file_id):
        url = f"https://file.stage.sensenova.cn/v1/files/{file_id}/content"
        response = requests.get(url, headers=self.headers)

        # 检查是否有重定向
        if response.history:
            url = response.url
        else:
            url = file_id
            # print("请求未被重定向，直接响应 URL:", response.url)

        return url

    def download_file_by_url(self, url, fn_path):
        response = requests.get(url)

        if response.status_code == 200:
            self.logger.info(f'downloading {fn_path}')
            with open(fn_path, 'wb') as file:
                file.write(response.content)
        else:
            raise Exception('Failed to download image url: ', url)

    def upload_file(self, fn_path, is_url=True):
        url = "https://file.stage.sensenova.cn/v1/files"

        headers = {
            "Authorization": f'Bearer {self.keys}'
        }

        data = {
            'description': 'string',
            'scheme': 'ASSISTANT_1'
        }

        # If file_source is a URL, download the image first
        if is_url:
            response = requests.get(fn_path)
            if response.status_code != 200:
                raise Exception("Failed to download the image from the URL")
            file_content = BytesIO(response.content)
            file_name = fn_path.split('/')[-1]
            files = {
                'file': (file_name, file_content)
            }
        else:
            
            if not os.path.exists(fn_path):
                raise Exception('local file path does not exist.')

            # Use the local file path without specifying MIME type
            files = {
                'file': (fn_path, open(fn_path, 'rb'))
            }

        response = requests.post(url, headers=headers, data=data, files=files)
        response = response.json()

        file_id = response['id']

        return file_id


    def _generate(
        self,
        input: str or PromptList,
        max_out_len: int = 512,
    ) -> str:
        """Generate results given an input.

        Args:
            inputs (str or PromptList): A string or PromptDict.
                The PromptDict should be organized in OpenCompass'
                API format.
            max_out_len (int): The maximum length of the output.

        Returns:
            str: The generated string.
        """
        assert isinstance(input, (str, PromptList))

        try:
            json_string = input.replace("'", '"')
            input_json=json.loads(json_string)
        except json.JSONDecodeError:
            messages = {'role': 'user', 'content': input}
        else:
            messages = {'role': 'user'}
            messages['file_ids'] = []
            for item in input_json:
                try:
                    if item['content'][0]['type'] == 'image_url':
                        url = item['content'][0]['image_url']['url']
                        file_id = self.upload_file(url, is_url=True)
                        messages['file_ids'].append(file_id)
                    elif  item['content'][0]['type'] == 'file_url':
                        url = item['content'][0]['file_url']['url']
                        file_id = self.upload_file(url, is_url=True)
                        messages['file_ids'].append(file_id)
                except:
                    messages['content'] = item['content']

        aid = self.create_assistant()
        tid = self.create_thread()

        if aid is None or tid is None:
            raise RuntimeError(f'Failed to create assistant:{aid} or thread:{tid}.')

        resp_msg = self.create_message(tid, messages)
        if resp_msg.status_code != 200:
            self.logger.error(f'create message failed: {str(resp_msg.json())}')
            return resp_msg.json()

        self.list_msgs_by_thread_id(tid)

        resp_run = self.create_run(aid, tid)
        if resp_run.status_code == 200:
            rid = resp_run.json().get("id")
        else:
            self.logger.error(f'create run id faled:  {str(resp_run.json())}')
            return resp_run.json()

        # wait to get results
        while True:
            sts = self.get_run_status(tid, rid)
            if sts == "completed" or sts == "failed":
                self.logger.info(f'Thread {tid} Running Status: {sts}')
                break

        resp = self.list_msgs_by_thread_id(tid)

        output_file_id = 'None'
        tool_call = 'None'
        content = 'None'
        out_file_url = 'None'
        
        for chunk in resp['messages'][0]['content']:
            if chunk.get('type') == 'tool_calls':
                tool_call =  chunk.get('tool_calls')[0]['name']
            elif chunk.get('type') == 'files':
                output_file_id = chunk.get('files')[0]
                out_file_url = self.get_file_url(output_file_id)
            elif chunk.get('type') == 'text':
                content = chunk.get('text')['value']

        if out_file_url != 'None':
            save_name = output_file_id + '.jpg'
            self.download_file_by_url(out_file_url, os.path.join(self.picture_cache_dir, save_name))

        msg_return = {
            'message': messages,
            'tool_call': tool_call,
            'output_file_id': output_file_id,
            'output_file_url': out_file_url,
            'content': content
        }

        return msg_return
