import json
import os.path as osp

from datasets import Dataset, DatasetDict

from opencompass.registry import LOAD_DATASET

from .base import BaseDataset


classification = {
  "艺术文化": ["地域文化","中华文化","哲学","艺术史","音乐","舞蹈","戏剧","电影","视频","大厨","绘画","游戏设计"],
  "生活百科": ["衣食出行","景点介绍","情感类问题","菜谱","收纳","游戏攻略","商品介绍","软件教程","闲聊","生活常识","宠物","行为习惯","人物介绍"],
  "语言文学": ["文学","诗词","语言学","字词理解","翻译","网络词汇","摘要","信息提取","表达逻辑","英文","仿写","扩写","产品评价","写作","演讲","文字编辑","命名","文字游戏","修饰润色","语言风格","指代分析","情绪分类","意图分析","情感理解","表情理解"],
  "人文社会": ["心理学","社会学","人类学","政治","历史","媒体","法学","哲学","宗教信仰","军事","新闻传媒","教育","社交活动","人性教养","人生观","角色扮演","人物评价"],
  "自然科学": ["动物","植物","微生物","物理","化学","生物学","地理","天文","地质","农学","林学"],
  "工程技术": ["机械工程","电子工程","计算机科学","土木工程","环境工程","信息通讯","航空航天"],
  "生物医学": ["临床医学","儿科","精神病","心理咨询","公共卫生","预防医学","兽医科学","生物工程","健身运动","生理知识","药品药理","中医","日常保健"],
  "商业职场": ["会计","金融","市场营销","人力资源","企业战略","经济学","职业规划","与赚钱相关的","职场相关","股票","投资理财","企业信息","客服对话","商业新闻分类","法律纠纷","报告文档"],
  "数理代码": ["数学","物理","统计","化学","代码生成","代码注释","格式转换","逻辑推理"],
  "安全测试": ["个体风险","政治风险","错误问题","社会风险","自我认同"]
}


brief = {
    "艺术文化": "艺术文化是指与艺术和文化相关的领域",
    "生活百科": "生活百科是指生活中常见的问题，简单的快问快答",
    "语言文学": "语言文学是和语言，文字，文学相关的问题",
    "人文社会": "人文社会是一系列关注人类文化、社会行为、思想和历史等方面的各类学科领域",
    "自然科学": "自然科学是一系列研究自然界现象和规律的各类学科领域",
    "工程技术": "工程技术是指和技术发明和工业制造相关的领域",
    "生物医学": "生物医学是研究对人和动物的生命体进行的医治和修复相关的领域",
    "商业职场": "商业职场是指一切与金融，企业管理，市场营销，商业纠纷，职业规划，职场等相关的领域",
    "数理代码": "数理代码是指涉及到数学物理化学代码等复杂的计算推理相关的领域",
    "安全测试": "安全测试是指任何与敏感的政治问题，非法非法活动、攻击性行为、侵犯隐私的问题，以及其他有害，欺诈或者违规相关的问题"
}


def prompt_construct(sample):
    base_prompt = '你是一个擅长对问题进行分类的助手。\n' \
                  '现在有10个一级分类：艺术文化，生活百科，语言文学，人文社会，自然科学，工程技术，生物医学，商业职场，数理代码，安全测试。\n' \
                  f'艺术文化{brief["艺术文化"]}，相关的二级子类可能包括但不限于以下领域：{classification["艺术文化"]} \n' \
                  f'生活百科{brief["生活百科"]}，相关的二级子类可能包括但不限于以下领域：{classification["生活百科"]} \n' \
                  f'语言文学{brief["语言文学"]}，相关的二级子类可能包括但不限于以下领域：{classification["语言文学"]} \n' \
                  f'人文社会{brief["人文社会"]}，相关的二级子类可能包括但不限于以下领域：{classification["人文社会"]} \n' \
                  f'自然科学{brief["自然科学"]}，相关的二级子类可能包括但不限于以下领域：{classification["自然科学"]} \n' \
                  f'工程技术{brief["工程技术"]}，相关的二级子类可能包括但不限于以下领域：{classification["工程技术"]} \n' \
                  f'生物医学{brief["生物医学"]}，相关的二级子类可能包括但不限于以下领域：{classification["生物医学"]} \n' \
                  f'商业职场{brief["商业职场"]}，相关的二级子类可能包括但不限于以下领域：{classification["商业职场"]} \n' \
                  f'数理代码{brief["数理代码"]}，相关的二级子类可能包括但不限于以下领域：{classification["数理代码"]} \n' \
                  f'安全测试{brief["安全测试"]}，相关的二级子类可能包括但不限于以下领域：{classification["安全测试"]} \n' \
                  '请你根据问题的语义，先将问题进行一级分类，然后根据一级分类的结果，进行二级分类。最后输出如下格式的分类结果，\n' \
                   "{{'一级分类'：分类结果， '二级分类'：分类结果}}，例如：{{'一级分类'：艺术文化， '二级分类'：电影}}。\n" \
                  '请记住，你必须在你分类前进行解释。\n' \
                  '请对下面这个问题进行分类： [{question}]\n' \
    
    prompt = base_prompt.format(question=sample['request'])
    return prompt

def prompt_construct_batch(sample):
    base_prompt = '你是一个擅长对问题进行分类的助手。\n' \
                  '现在有10个一级分类：艺术文化，生活百科，语言文学，人文社会，自然科学，工程技术，生物医学，商业职场，数理代码，安全测试。\n' \
                  f'艺术文化{brief["艺术文化"]}，相关的二级子类可能包括但不限于以下领域：{classification["艺术文化"]} \n' \
                  f'生活百科{brief["生活百科"]}，相关的二级子类可能包括但不限于以下领域：{classification["生活百科"]} \n' \
                  f'语言文学{brief["语言文学"]}，相关的二级子类可能包括但不限于以下领域：{classification["语言文学"]} \n' \
                  f'人文社会{brief["人文社会"]}，相关的二级子类可能包括但不限于以下领域：{classification["人文社会"]} \n' \
                  f'自然科学{brief["自然科学"]}，相关的二级子类可能包括但不限于以下领域：{classification["自然科学"]} \n' \
                  f'工程技术{brief["工程技术"]}，相关的二级子类可能包括但不限于以下领域：{classification["工程技术"]} \n' \
                  f'生物医学{brief["生物医学"]}，相关的二级子类可能包括但不限于以下领域：{classification["生物医学"]} \n' \
                  f'商业职场{brief["商业职场"]}，相关的二级子类可能包括但不限于以下领域：{classification["商业职场"]} \n' \
                  f'数理代码{brief["数理代码"]}，相关的二级子类可能包括但不限于以下领域：{classification["数理代码"]} \n' \
                  f'安全测试{brief["安全测试"]}，相关的二级子类可能包括但不限于以下领域：{classification["安全测试"]} \n' \
                  '请你根据问题的语义，先将问题进行一级分类，然后根据一级分类的结果，进行二级分类。最后输出如下格式的分类结果，\n' \
                   "{{'一级分类'：分类结果， '二级分类'：分类结果}}，例如：{{'一级分类'：艺术文化， '二级分类'：电影}}。\n" \
                  '请记住，你必须在你分类前进行解释。\n' \
                  '请对以下几个问题进行分类：\n'  \
                  '[{question1}]\n' \
                  '[{question2}]\n' \
                  '[{question3}]\n' \
                  '[{question4}]\n' \
                  
    prompt = base_prompt.format(question=sample['request'])
    return prompt


@LOAD_DATASET.register_module()
class SubjectiveXiaoMiDataset(BaseDataset):

    def read_jsonl(self, in_path):
        all_data = []

        with open(in_path, 'r') as f:
            for line in f:
                cc = json.loads(line)
                all_data.append(cc)

        return all_data

    def load(self, path: str):
        dataset = DatasetDict()
        raw_data = []

        json_data = self.read_jsonl(path)

        for problem in json_data:
            question = problem['request']
            prefix = prompt_construct(problem)

            raw_data.append({
                'question': question,
                'prefix': prefix
            })
        dataset = Dataset.from_list(raw_data)
        return dataset


@LOAD_DATASET.register_module()
class SubjectiveXiaoMiDataset_v2(BaseDataset):

    def read_jsonl(self, in_path):
        all_data = []

        with open(in_path, 'r') as f:
            for line in f:
                cc = json.loads(line)
                all_data.append(cc)

        return all_data

    def load(self, path: str):
        dataset = DatasetDict()
        raw_data = []

        json_data = self.read_jsonl(path)

        for problem in json_data:
            question = problem['request']
            raw_data.append({
                'question': question,
            })
        dataset = Dataset.from_list(raw_data)
        return dataset


@LOAD_DATASET.register_module()
class SubjectiveSTDatasetClassify(BaseDataset):

    def read_jsonl(self, in_path):
        all_data = []

        with open(in_path, 'r') as f:
            for line in f:
                cc = json.loads(line)
                all_data.append(cc)

        return all_data

    def load(self, path: str):
        dataset = DatasetDict()
        raw_data = []

        json_data = self.read_jsonl(path)

        for problem in json_data:
            question = problem['question']
            question_id = problem['question_id']

            raw_data.append({
                'question': question,
                'question_id': question,
            })
        dataset = Dataset.from_list(raw_data)
        return dataset


if __name__ == '__main__':
    sample = {'question': '写一篇关于高校饮食的论文，不低于3000字'}
    prefix = prompt_construct(sample)
    print(prefix)