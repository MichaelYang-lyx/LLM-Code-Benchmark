import pandas
from operator import add
from components.Eval.BLEU import codebleu_score, code_postprocess
import json
from models.openAI_api import OpenAI
import os
import sys
import importlib.util
from tqdm import tqdm
import contextlib
from components.Eval.BLEU import codebleu_score
# ======

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
conf = SparkConf().setAppName("AItest")
sc = SparkContext(conf=conf)
spark = SparkSession(sc)

# =====


THIS_DIR = './jobs/1AI_test_try'
TARGET_DIR = './data/AItest'
JSON_FILE = os.path.join(TARGET_DIR, 'AI.json')
OUTPUT_DIR = os.path.join(THIS_DIR, 'output')
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
# Get all subfolders in the current directory
folders = [f.name for f in os.scandir(TARGET_DIR) if f.is_dir()]

# Filter out subfolders starting with 'test'
test_folders = [folder for folder in folders if folder.startswith('test')]


def get_score(data_folder):
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

    log = os.path.join(OUTPUT_DIR, 'log.txt')

    if not os.path.exists(data_folder):

        try:
            with open(log, 'a') as f, contextlib.redirect_stdout(f):
                print("---------- Running ", main_file, " ----------")
                spec.loader.exec_module(module)
                score = module.main()  # Assume main function returns score

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
                print(
                    f"Did not find reference.txt file in {data_folder} folder")

            score = codebleu_score(solution_content, reference_content)[
                'codebleu']
        # Remove the directory of main.py from sys.path
        sys.path.remove(os.path.join(TARGET_DIR, data_folder))

    else:
        print(f"Did not find main.py file in {data_folder} folder")

    # get solution and reference content

    return score


# -------------------- infer ----------------------------
base_prompt = '你是一个擅长补充代码的助手。\n请你根据题目要求来完善代码。' \
    '请记住，你必须在题目代码的框架下进行回答，需要包含框架并且最后输出是一整段完整代码(包含框架import内容)。\n' \
    '你只需关注代码部分,不需要关注环境配置等问题。请你以\'\'\'{language} {code}\'\'\'的格式回答。\n' \
    '[需要补充的代码框架]： {question}\n' \



languages = []
questions = []


def infer(item):

    prompt = base_prompt.format(
        language=item['language'], code='{you code here}', question=item['question'])
    solution_path = os.path.join(
        TARGET_DIR, 'test'+str(item['question_id']), 'solution.py')

    # 没有才生成
    if not os.path.exists(solution_path):
        api = OpenAI()
        result = code_postprocess(api.generate(prompt))
        with open(solution_path, 'w') as f:
            f.write(result)
    return solution_path


def get_questions(json_file):
    # Load the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)
    rdd = sc.parallelize(data)
    solution_paths = rdd.map(infer)
    print(solution_paths.collect())


# Call the function
get_questions(JSON_FILE)


# -------------------- eval ----------------------------


def evaluate(test_folder):
    score = get_score(test_folder)
    return (test_folder, score)


test_folders_rdd = spark.sparkContext.parallelize(test_folders)
result_rdd = test_folders_rdd.map(evaluate)


# -------------------- summary ----------------------------

# 计算总分数
total_score = result_rdd.map(lambda x: x[1]).reduce(add)

# 计算文件夹的数量
num_folders = result_rdd.count()

# 计算平均分数
average_score = total_score / num_folders
print('result:', result_rdd.collect())
print("Average score: ", average_score)
# 将 RDD 转换为 DataFrame
result_df = result_rdd.toDF()
pandas_df = result_df.toPandas()
pandas_df.to_excel(os.path.join(OUTPUT_DIR, 'summary.xlsx'), index=False)
