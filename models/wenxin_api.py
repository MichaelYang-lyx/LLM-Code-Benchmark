import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class Wenxin:
    def __init__(self):
        self.api_key = 'DwR2IFbML8YoLEUGMdYfnRGa'
        self.secret_key = os.getenv("BAIDU_SECRET_KEY")
        self.access_token = self.get_access_token()
    
    def get_access_token(self):
        """
        使用 API Key 和 Secret Key 获取 access_token。
        """
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}"
        
        payload = json.dumps("")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.post(url, headers=headers, data=payload)
        return response.json().get("access_token")

    def generate(self, prompt, model_version='ernie-speed-128k'):
        """
        从文心模型生成响应。

        参数:
        prompt (str): 要发送给模型的提示。
        model_version (str): 要使用的文心模型版本。默认为 'ernie-speed-128k'。

        返回:
        str: 模型的响应内容。
        """
        base_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/"
        url = f"{base_url}{model_version}?access_token={self.access_token}"

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, headers=headers, data=payload)
        response_data = response.json()
        
        # 打印响应以进行调试
        print("Debug: Response JSON:", response_data)
        
        # 根据实际的响应结构进行调整
        if 'result' in response_data:
            return response_data['result']
        elif 'error' in response_data:
            return f"Error: {response_data['error']}"
        else:
            return "Unexpected response structure"

