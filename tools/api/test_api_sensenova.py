# -*- coding: utf-8 -*-
import requests
import json
import urllib3
import os
print(os.getcwd())

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from opencompass.models.internLM2.tools_buildin import tools_define_buildin_0131_no_interpreter

url = "https://api.stage.sensenova.cn/v1/llm/chat-completions"
key = os.getenv('SENSENOVA_API_KEY')

headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {key}'
}


text = '画一个凤凰飞天的图像'

stream = False

data = {
    "model": "SenseChat-stage-fc",
    "messages": [
      {
        "role": "user",
        "content": f"{text}", 
      }
    ],
    "tools": tools_define_buildin_0131_no_interpreter,
    "tool_choice": {
        "mode": "auto"
    },
    "temperature": 0.8,
    "top_p": 0.7,
    "max_new_tokens": 1000,
    "repetition_penalty": 1.05,
    "know_ids": [],
    "stream": stream,
    "user": "#*#*SenseConnerFree*#*#"
  }
   
response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
print('request-id: ', response.headers.get('X-Request-Id'))

if stream:
  if response.status_code == 200:
    response.encoding = 'utf-8'
    response_text = response.text

    print(response_text)
    data_blocks = response_text.split("data:")
    data_blocks = data_blocks[1:]


    out = ""
    for i, part in enumerate(data_blocks):
        print(f'process {i}: {part}')
        try:
            if part.startswith('[DONE]'):
              print('finish')
              break

            json_data = json.loads(part)
            choices = json_data["data"]["choices"]
            for c in choices:
              delta=c.get("delta")
              out += delta
        except json.decoder.JSONDecodeError as e:
          print(f"Error decoding JSON: {part}")

    # print(out)
  else:
      print('Error:', response.status_code, response.text)

else:
  if response.status_code == 200:
      print(response.json()['data']['choices'][0]['message'])
  else:
      print('Error:', response.status_code, response.text)
