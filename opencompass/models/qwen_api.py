import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Union

import requests
import os
import dashscope

from opencompass.utils.prompt import PromptList

from .base_api import BaseAPIModel

PromptType = Union[PromptList, str]


class Qwen(BaseAPIModel):
    """Model wrapper around Qwen.

    Documentation: https://help.aliyun.com/zh/dashscope/developer-reference/tongyiqianwen-large-language-models

    Args:
        model_type (str): The type of the model
            e.g. `chat`
        secretkey (str): secretkey in order  to obtain access_token
        key (str): Authorization key.
        query_per_second (int): The maximum queries allowed per second
            between two consecutive calls of the API. Defaults to 1.
        max_seq_len (int): Unused here.
        meta_template (Dict, optional): The model's meta prompt
            template if needed, in case the requirement of injecting or
            wrapping of any meta instructions.
        retry (int): Number of retires if the API call fails. Defaults to 2.
    """

    def __init__(self,
                 path: str,
                 key: str,
                 query_per_second: int = 2,
                 max_seq_len: int = 2048,
                 meta_template: Optional[Dict] = None,
                 retry: int = 2,
                 generation_kwargs: Dict = {
                     'temperature': 0.8,
                 }):
        super().__init__(path=path,
                         max_seq_len=max_seq_len,
                         query_per_second=query_per_second,
                         meta_template=meta_template,
                         retry=retry,
                         generation_kwargs=generation_kwargs)
        self.model = path
        self.key = key
        # dashscope.api_key = self.key



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
        """
        {
          "messages": [
            {'role': 'system', 'content': 'You are a helpful assistant.'}
            {'role': 'user', 'content': '如何做西红柿炒鸡蛋？'}
          ]
        }

        """


        if isinstance(input, str):
            messages = [{'role': 'user', 'content': input}]
        else:
            messages = []
            for item in input:
                msg = {'content': item['prompt']}
                if item['role'] == 'user' or item['role'] == 'HUMAN':
                    msg['role'] = 'user'
                elif item['role'] == 'system' or item['role'] == 'SYSTEM':
                    msg['role'] = 'system'
                elif item['role'] == 'assistant' or item['role'] == 'BOT':
                    msg['role'] = 'assistant'

                messages.append(msg)
        data = {'messages': messages}
        data.update(self.generation_kwargs)

        max_num_retries = 0
        while max_num_retries < self.retry:
            self.acquire()

            max_num_retries += 1
            raw_response = dashscope.Generation.call(
                model=self.model,
                messages=messages,
                # set the random seed, optional, default to 1234 if not set
                result_format='message',  # set the result to be "message" format.
            )

            response = raw_response
            self.release()

            if response is None:
                print('Connection error, reconnect.')
                # if connect error, frequent requests will casuse
                # continuous unstable network, therefore wait here
                # to slow down the request
                self.wait()
                continue
        
            if raw_response.status_code == 200:
                msg = response['output']['choices'][0]['message']['content'].strip()
                return msg
            elif raw_response.status_code == 400:
                if raw_response.code == 'DataInspectionFailed':
                    return 'unsafe'
            else:
                print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                    raw_response.request_id, raw_response.status_code,
                    raw_response.code, raw_response.message
                ))
                time.sleep(1)
                continue
            
        raise RuntimeError(raw_response.message)
