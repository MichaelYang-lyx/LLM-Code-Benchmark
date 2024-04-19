import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()
# 你的Sensenova API URL和密钥
url = "https://api.stage.sensenova.cn/v1/llm/chat-completions"
key = os.getenv('SENSENOVA_API_KEY')

# 聊天消息
messages = [{"role": "user", "content": "Say this is a test!"}]

# 请求头部
headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

# 请求体
data = {
    "model": "gpt-4",
    "messages": messages
}

# 发送POST请求
response = requests.post(url, headers=headers, data=json.dumps(data))

# 解析响应
response_data = response.json()

print(response_data)
