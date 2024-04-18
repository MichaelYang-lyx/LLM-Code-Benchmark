import json
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional
from urllib import response

import requests

from opencompass.registry import MODELS
from opencompass.utils.logging import get_logger

from .base_api import BaseAPIModel
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@MODELS.register_module()
class LunzongAPI(BaseAPIModel):

    is_api: bool = True

    def __init__(
            self,
            url: str,
            key: str,
            input_format: str,
            path: str = 'LunzongAPI',
            max_seq_len: int = 8192,
            stop_sign: str = '',
            system_prompt: str = '',
            meta_template: Optional[Dict] = None,
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

    def generate(self, inputs: List[str], max_out_len: int,
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

    def _generate(self, input: str, max_out_len: int) -> str:
        max_num_retries = 0
        while max_num_retries < self.retry:
            self.wait()
            try:
                input = self.input_format.replace("<input_text_to_replace>", input)
                if self.system_prompt:
                    data = dict(inputs=input, parameters=self.parameters, system_prompt=self.system_prompt, stream=True)
                else:
                    data = dict(inputs=input, parameters=self.parameters, stream=True)
                raw_response = requests.post(self.url,
                                             headers=self.headers,
                                             data=json.dumps(data),
                                             verify=False)

            except requests.ConnectionError:
                self.logger.error('Got connection error, retrying...')
                continue
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