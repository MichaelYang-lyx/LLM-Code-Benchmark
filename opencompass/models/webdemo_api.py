# -*- coding: utf-8 -*-
import json
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional
from urllib import response
import re

import requests

from opencompass.registry import MODELS
from opencompass.utils.logging import get_logger
from opencompass.utils.prompt import PromptList

from .base_api import BaseAPIModel
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


'''
For temporary interpreter api provided by shenghu
'''
@MODELS.register_module()
class WebDemoAPI(BaseAPIModel):

    is_api: bool = True

    def __init__(
            self,
            url: str,
            key: str,
            input_format: str,
            path: str = 'WebDemoAPI',
            max_seq_len: int = 8192,
            stop_sign: str = '',
            meta_template: Optional[Dict] = None,
            system_prompt: str = '',
            retry: int = 2,
            parameters: Optional[Dict] = None,
    ):

        super().__init__(path=path,
                         max_seq_len=max_seq_len,
                         meta_template=meta_template,
                         retry=retry)
        self.logger = get_logger()
        self.url = url
        self.headers = {'Content-Type': 'application/json'}
        if key:
            self.headers['Authorization'] = f'Bearer {key}'
        self.input_format = input_format
        self.parameters = parameters
        self.stop_sign = stop_sign
        self.system_prompt = system_prompt
        self.logger.info(f'self.url : {self.url}')
        self.logger.info(f'self.headers : {self.headers}')
        self.logger.info(f'self.input_format : {self.input_format}')
        self.logger.info(f'self.parameters : {self.parameters}')

    def generate(self, inputs: List[str or PromptList], max_out_len: int,
                 **kwargs) -> List[str]:
        """Generate results given a list of inputs.

        Args:
            inputs (List[str]): A list of strings or PromptDicts.
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
        return results

    def _generate(self, input: List[str or PromptList], max_out_len: int) -> str:
        max_num_retries = 0
        while max_num_retries < self.retry:
            self.wait()
            try:
                if isinstance(input, str):
                    messages = [{'role': 'user', 'content': input}]
                else:
                    messages = []
                    for item in input:
                        tmp_input = self.input_format.replace("<input_text_to_replace>", item['prompt'])
                        msg = {'content': tmp_input}
                        if item['role'] == 'HUMAN':
                            msg['role'] = 'user'
                        elif item['role'] == 'BOT':
                            msg['role'] = 'assistant'
                        elif item['role'] == 'SYSTEM':
                            msg['role'] = 'system'
                        messages.append(msg)
                
                if self.system_prompt:
                    data = dict(messages=messages, parameters=self.parameters, system_prompt=self.system_prompt, stream=False)
                else:
                    data = dict(messages=messages, parameters=self.parameters, stream=False)
                    
                raw_response = requests.post(self.url,
                                             headers=self.headers,
                                             data=json.dumps(data),
                                             verify=False)

            except requests.ConnectionError:
                self.logger.error('Got connection error, retrying...')
                continue

            if not data['stream']:
                response = raw_response.json()

                if raw_response.status_code == 200:
                    msg = response['new_messages']
                    return msg

            # TODO: Stream mode not yet supported.
            try: 
                if self.headers.get('Authorization', None) is not None:
                    for chunk in raw_response.iter_lines():
                        chunk = chunk.decode()
                        if chunk == '':
                            continue
                        chunk = json.loads(chunk[5:])
                        if chunk['generated_text']:
                            generated_text = chunk['generated_text']
                    
                else:
                    if raw_response.status_code == 200:
                        generated_text =  raw_response.json()['generated_text'][0]
                        
                    else:
                        self.logger.error('Call API Error:', raw_response.status_code, raw_response.text)

                # stop when meet the stop_sign
                if self.stop_sign != "":
                    generated_text = generated_text.split(self.stop_sign)[0]

                return generated_text

            except requests.JSONDecodeError:
                self.logger.error('JsonDecode error, got',
                                  str(raw_response.content))
            except KeyError:
                self.logger.error('KeyError, got',
                                  str(raw_response.content))
            max_num_retries += 1

        raise RuntimeError('Calling LunzongAPI failed after retrying for '
                           f'{max_num_retries} times. Check the logs for '
                           'details.')
    
'''
For temporary assistant api provided by ruihao (synchronized mode)
'''
@MODELS.register_module()
class WebDemoAPI2(BaseAPIModel):
    is_api: bool = True

    def __init__(
            self,
            url: str,
            key: str,
            model: str,
            input_format: str,
            code_agent: str,
            path: str = 'WebDemoAPI2',
            max_seq_len: int = 8192,
            stop_sign: str = '',
            meta_template: Optional[Dict] = None,
            system_prompt: str = '',
            retry: int = 2,
            parameters: Optional[Dict] = None,
    ):

        super().__init__(path=path,
                         max_seq_len=max_seq_len,
                         meta_template=meta_template,
                         retry=retry)
        self.logger = get_logger()
        self.url = url
        self.headers = {'Content-Type': 'application/json',
                        'X-Accel-Buffering': 'no'
                        }
        if key:
            self.headers['Authorization'] = f'Bearer {key}'
        self.input_format = input_format
        self.parameters = parameters
        self.code_agent = code_agent
        self.stop_sign = stop_sign
        self.system_prompt = system_prompt
        self.model = model
        self.logger.info(f'self.url : {self.url}')
        self.logger.info(f'self.headers : {self.headers}')
        self.logger.info(f'self.input_format : {self.input_format}')
        self.logger.info(f'self.parameters : {self.parameters}')


    def generate(self, inputs: str, max_out_len: int,
                 **kwargs) -> List[str]:
        """Generate results given a list of inputs.

        Args:
            inputs (List[str]): A list of strings or PromptDicts.
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
        return results

    def _generate(self, input: str , max_out_len: int) -> str:
        max_num_retries = 0

        while max_num_retries < self.retry:
            self.wait()
            message=[]
            try:
                json_string = input.replace("'", '"')
                input_json=json.loads(json_string)
            except json.JSONDecodeError:
                    print("The string is not valid JSON.")
                    query=input
            else:
                # separate the input into query and messages
                for item in input_json:
                    if isinstance(item['content'], list):
                        message.append(item)
                    else:
                        query = item['content']
            try:
                data = {
                    'query': query,
                    'messages': message,
                    'model': self.model,
                    'code_agent': self.code_agent
                }
                
                raw_response = requests.post(self.url,
                                             headers=self.headers,
                                             json=data,
                                             stream=True)


            except requests.ConnectionError:
                self.logger.error('Got connection error, retrying...')
                continue

            if raw_response.status_code == 200:

                ret = []
                event = None
                for chunk in raw_response.iter_lines(decode_unicode=True):
                    if chunk:
                        if chunk.startswith('event: '):
                            event = chunk.strip('event: ')
                        elif chunk.startswith('data: ') and (event == 'RESPONSE' or event == 'TOOL_CALL_RESPONSE'):
                            data = json.loads(chunk.strip('data: '))
                            ret.append(data)
                return ret