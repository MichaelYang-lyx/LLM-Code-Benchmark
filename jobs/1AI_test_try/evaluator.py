import os
import sys
import importlib.util
from tqdm import tqdm
import contextlib
from components.Eval.BLEU import  codebleu_score

THIS_DIR = './jobs/1AI_test_try'
TARGET_DIR='./data/AItest'
JSON_FILE=os.path.join(TARGET_DIR,'AI.json')

# Get all subfolders in the current directory
folders = [f.name for f in os.scandir(TARGET_DIR) if f.is_dir()]

# Filter out subfolders starting with 'test'
test_folders = [folder for folder in folders if folder.startswith('test')]

def get_score(data_folder,output_dir):
    main_file = os.path.join(TARGET_DIR, data_folder, 'main.py')
    solution_file = os.path.join(TARGET_DIR, data_folder, 'solution.py')  
    reference_file = os.path.join(TARGET_DIR, data_folder, 'reference.txt')  
    
    if os.path.isfile(main_file):
        # Add the directory of main.py to sys.path
        if "main" in sys.modules:
            del sys.modules["main"]
        if "solution" in sys.modules:
            del sys.modules["solution"]
        sys.path.insert(0, os.path.join(TARGET_DIR, data_folder))
        spec = importlib.util.spec_from_file_location("main", main_file)
        module = importlib.util.module_from_spec(spec)

    log=os.path.join(output_dir, 'log.txt')
    
    if not os.path.exists(data_folder):

        try:
            with open(log, 'a') as f, contextlib.redirect_stdout(f):
                print("---------- Running ", main_file, " ----------")
                spec.loader.exec_module(module)
                score = module.main()  # Assume main function returns score
            print(f"Score: {score}")
        except Exception as e:
            print(f"Running {main_file} error: {str(e)}")
            
            
            # Use another way to calculate score here
            if os.path.isfile(solution_file):  
                with open(solution_file, 'r') as f:  
                    solution_content = f.read()  
            else:
                print(f"Did not find solution.py file in {data_folder} folder")  
                
            if os.path.isfile(reference_file):
                with open(reference_file, 'r') as f:
                    reference_content = f.read()
            else:
                print("Did not find reference.txt file in {data_folder} folder")
                    
            score = codebleu_score(solution_content, reference_content)['codebleu']
            print(f"Score calculated using backup method: {score}")
        # Remove the directory of main.py from sys.path
        sys.path.remove(os.path.join(TARGET_DIR, data_folder))
    

    else:
        print(f"Did not find main.py file in {data_folder} folder")

    # get solution and reference content
    

    return score




##===-------

from models.openAI_api import OpenAI
import json
api = OpenAI()
from components.Eval.BLEU import codebleu_score, code_postprocess

base_prompt = '你是一个擅长补充代码的助手。\n请你根据题目要求来完善代码。' \
    '请记住，你必须在题目代码的框架下进行回答，需要包含框架并且最后输出是一整段完整代码(包含框架import内容)。\n' \
    '你只需关注代码部分,不需要关注环境配置等问题。请你以\'\'\'{language} {code}\'\'\'的格式回答。\n' \
    '[需要补充的代码框架]： {question}\n' \

# -------------------- infer ----------------------------


# -------------------- eval ----------------------------

languages=[]
questions=[]
def get_questions(json_file):
    # Load the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Iterate over all items in the data
    for item in tqdm(data, desc="Infer"):
    # Print the question field
        prompt = base_prompt.format(language=item['language'], code='{you code here}',question=item['question'])
        test_dir=os.path.join(TARGET_DIR, 'test'+str(item['question_id']),'t.py')
        
        result=code_postprocess(api.generate(prompt))

        # 把result输入test_dir
        with open(test_dir, 'w') as f:
            f.write(result)

        

# Call the function
get_questions(JSON_FILE)
print(test_folders)
##---------



# for folder in tqdm(test_folders, desc="Eval", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
#     output_dir = os.path.join(THIS_DIR, 'output')
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir  )
#     score = get_score(folder,output_dir)
