from models.openAI_api import OpenAI
import json
api = OpenAI()


base_prompt = '你是一个擅长补充代码的助手。\n请你根据题目要求来完善代码。' \
    '请记住，你必须在题目代码的框架下进行回答，需要包含框架并且最后输出是一整段完整代码(包含框架import内容)。\n' \
    '你只需关注代码部分,不需要关注环境配置等问题。请你以\'\'\'{language} {code}\'\'\'的格式回答。\n' \
    '[需要补充的代码框架]： {question}\n' \

# -------------------- infer ----------------------------
data_config={
    'path':'./data/AItest/AI.json'
}

# -------------------- eval ----------------------------

languages=[]
questions=[]
def get_questions(data_config):
    # Load the JSON file
    with open(data_config['path'], 'r') as f:
        data = json.load(f)

    # Iterate over all items in the data
    for item in data:
        # Print the question field
        prompt = base_prompt.format(language=item['language'], code='{you code here}',question=item['question'])
        print(prompt)


# Call the function
get_questions(data_config)



# ----------------- summarizer -------------------------


#print(api.generate('今天深圳天气怎么样'))