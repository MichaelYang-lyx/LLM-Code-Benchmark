from datetime import datetime
import json


def get_time():
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %A %H:%M %p")
    return formatted_time


system_prompt_v2 = "你是SenseChat，一个由商汤科技开发的人工智能助手，可以利用各种工具来辅助解答各种问题。你可以同时调用多个工具，也可以顺序调用工具，遇到图片链接可以当做真实的图片，图片链接应该包含所有的参数，你的答复应尽量使用中文。请尽量优化你的回答，确保信息的准确性和有用性以及简洁性。不依赖工具的问题可以直接回答。如果工具的最新回答有图片链接，你需要用markdown格式展示出来。当用户上传数据或者表格文件时，你需要调用data_analysis数据分析工具来回答。当用户有数学推理之类的问题时，你需要调用python_interpreter工具来回答。针对图片的问题你需要从历史对话中提取正确的图片链接，调用vqa_agent来回答。"
sys_prompt_v2 = f"<system>: <|timer|>:{get_time()}\n"+f'<|profile|>: {system_prompt_v2}'


def load_file(filepath):
    if filepath.endswith('json'):
        f = open(filepath, 'r')
        data_list = json.load(f)
    elif filepath.endswith('jsonl'):
        data_list = []
        with open(filepath, 'r') as file:
            for line in file:
                data_list.append(json.loads(line))
    return data_list

def save_file(data_list, save_file, ensure_ascii=False):
    with open(save_file, "w") as f:
        json.dump(data_list, f, indent=2, ensure_ascii=ensure_ascii)



# temp hard code, convert data/data_0110/msagnet_sub19_sample_1k.jsonl to openai, otherwise, refused by minimax 
def convert_to_openai_format(tool_dict):
    tool_parameters = {
        "properties": tool_dict['properties'],
        "required": tool_dict['required'],
        "type": "object"
    }
    openai_dict = {
        "function": {
            "description": tool_dict['description'],
            "name": tool_dict['name'],
            "parameters": tool_parameters,
        },
        "type": "function"
    }
    return openai_dict
