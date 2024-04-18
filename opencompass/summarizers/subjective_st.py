# flake8: noqa: E501
import csv
import os
import os.path as osp
import re
from collections import defaultdict
from datetime import datetime
import json

import mmengine
import numpy as np
from mmengine import ConfigDict
import pandas as pd

try:
    from prettytable import from_csv
except ImportError:
    from_csv = None

from opencompass.utils import dataset_abbr_from_cfg, model_abbr_from_cfg


all_dimensions = [
    '事实正确性', '满足用户需求', '安全无害', '清晰度', '逻辑性', '完备性', '创造性', '可负责程度', '逻辑连贯性',
    '公平与可负责程度', '丰富度', '综合得分'
]



def post_process(judgment: str):

    def extract_rating(text):
        pattern = r'{(.*?)}(?![^{]*{)'  # match last brackets
        match = re.search(pattern, text)

        if match:
            dictionary_str = match.group(1)
            kv_pattern = r"'(.*?)': (-1|\d+)"
            matches = re.findall(kv_pattern, dictionary_str)
            result_dict = {key: int(value) for key, value in matches}

            return result_dict
        else:
            return None

    def extract_score(text):
        pattern = r'\'综合得分\': (\d+(\.\d{1,2})?)'
        match = re.search(pattern, text)
        if match:
            return float(match.group(1))
        return -1

    def check_rating(rating):
        for k, v in rating.items():
            if isinstance(v, (int, float)) and k in all_dimensions:  # 确保值是数字
                if v >= -1 and v <= 10:
                    pass
                else:
                    return None
            else:
                return None
        return rating

    judgment = judgment.replace('\n', '')
    rating = extract_rating(judgment)

    if rating is not None:
        score = rating.get('综合得分', -1)
        if score == -1:
            score = extract_score(judgment)
        if score >= 0 and score <= 10:
            pass
        else:
            score = -1
        rating = check_rating(rating)
    else:
        score = -1
    return rating, score

def post_process_r4(judgment):

    def extract_rating(text):
        # pattern = r'{(.*?)}(?![^{]*{)'  # match last brackets - TODO \{[^{}]*\}$
        pattern = r"\{([^\{\}]*)\}(?=[^\{\}]*$)"
        match = re.findall(pattern, text)
        if match:
            dictionary_str = match[-1]
            # print(dictionary_str)

            kv_pattern = r"'(.*?)': (.*)"
            # kv_pattern = r"'(.*?)'[:：]\s*([^,]*)"

            matches = re.findall(kv_pattern, dictionary_str)
            # print(matches)

            result_dict = {key: value.strip("'") for key, value in matches}

            return result_dict
        else:
            return None





    judgment = judgment.replace('\n', '')
    rating = extract_rating(judgment)

    return rating, -1




class SubjectiveSTSummarizer:
    """Do the subjectivity analyze based on evaluation results.

    Args:
        config (ConfigDict): The configuration object of the evaluation task.
            It's expected to be filled out at runtime.
    """

    def __init__(self, config: ConfigDict) -> None:
        self.tasks = []
        self.cfg = config
        self.eval_model_cfgs = self.cfg['eval']['partitioner']['models']
        self.eval_model_abbrs = [
            model_abbr_from_cfg(model) for model in self.eval_model_cfgs
        ]
        self.judge_abbr = model_abbr_from_cfg(self.cfg['judge_model'])

    def summarize_excel(self, time_str: str = datetime.now().strftime('%Y%m%d_%H%M%S')):
        dataset_cfgs = self.cfg['datasets']
        work_dir = self.cfg['work_dir']
        self.work_dir = work_dir

        self.time_str = time_str
        output_path = osp.join(self.work_dir, 'summary',
                               f'summary_{self.time_str}.txt')
        output_dir = osp.join(osp.split(output_path)[0], f'{self.time_str}')
        mmengine.mkdir_or_exist(output_dir)        

        # cp base excel to summary folder
        base_excel_path = './data/subjective/subjective_988_base_r3.xlsx'
        dst_excel_path = f'{output_dir}/base.xlsx'
        os.system(f'cp {base_excel_path} {dst_excel_path}')


        fout = osp.join(output_dir, 'summary.csv')

        fout_flag = 0
        out_excel_path = osp.join(output_dir, 'summary.xlsx')



        results_folder = osp.join(work_dir, 'results')
        prediction_folder = osp.join(work_dir, 'predictions')

        for subdir in os.listdir(prediction_folder):
            if subdir not in self.eval_model_abbrs:
                continue
            
            model_abbr = subdir
            subdir_eval_path = os.path.join(results_folder, subdir) + '_judged-by--' + self.judge_abbr
            subdir_pred_path = os.path.join(prediction_folder, subdir)

            if os.path.isdir(subdir_eval_path):
                model = subdir
                for dataset in dataset_cfgs:
                    dataset_abbr = dataset_abbr_from_cfg(dataset)
                    eval_filepath = os.path.join(subdir_eval_path,
                                            dataset_abbr + '.json')
                    result = mmengine.load(eval_filepath)

                    pred_filepath = os.path.join(subdir_pred_path,
                                            dataset_abbr + '.json')
                    preds = mmengine.load(pred_filepath)


                    base_data = pd.read_excel(dst_excel_path)

                    # Load results
                    judged_answers = []
                    for k, v in result.items():
                        prediction = preds[k]['prediction']
                        rating, score = post_process(v['prediction'])
                        question_id = str(v['gold'])


                        row = base_data[base_data['序号'] == question_id]

                        # prevent illegal char in prediction
                        ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
                        prediction = ILLEGAL_CHARACTERS_RE.sub(r'', prediction)

                        base_data.loc[row.index, model_abbr] = prediction

                        if rating is not None: # and score != -1:
                            judged_answers.append({
                                'rating': rating,
                                'score': score
                            })

                            # write results to base dataframe
                            row = base_data[base_data['序号'] == str(question_id)]
                            for rating_k, rating_v in rating.items():
                                base_data.loc[row.index, rating_k] = rating_v
                            base_data.loc[row.index, '综合得分'] = score

                    print(
                        f'Among {len(result)} judgements, successfully extracted {len(judged_answers)} judgements.'
                    )

                    # 初始化一个嵌套字典用于存储模型和评分
                    dimension_ratings = defaultdict(int)
                    dimension_counts = defaultdict(int)

                    for ans in judged_answers:
                        for k, v in ans['rating'].items():
                            if k != '综合得分':
                                if v != -1: # ignore the -1
                                    dimension_ratings[k] += v
                                    dimension_counts[k] += 1
                        dimension_ratings['综合得分'] += ans['score']
                        dimension_counts['综合得分'] += 1

                    # average score
                    dimension_avg_ratings = defaultdict(float)
                    for dimension, total_score in dimension_ratings.items():
                        dimension_avg_ratings[
                            dimension] = total_score / dimension_counts[
                                dimension]

                    scores = {model: dimension_avg_ratings}

                    rows = list(scores.keys())
                    columns = list(scores[rows[0]].keys())
                    with open(fout, 'a+', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        if fout_flag == 0:
                            writer.writerow(['模型'] + columns)
                            fout_flag += 1
                        for row in rows:
                            writer.writerow(
                                [row] +
                                [scores[row][column] for column in columns])
                            
                    base_data.to_excel(out_excel_path)

    def summarize_excel_r4(self, time_str: str = datetime.now().strftime('%Y%m%d_%H%M%S')):
        dataset_cfgs = self.cfg['datasets']
        work_dir = self.cfg['work_dir']
        self.work_dir = work_dir

        self.time_str = time_str
        output_path = osp.join(self.work_dir, 'summary',
                               f'summary_{self.time_str}.txt')
        output_dir = osp.join(osp.split(output_path)[0], f'{self.time_str}')
        mmengine.mkdir_or_exist(output_dir)        

        # cp base excel to summary folder
        base_excel_path = './data/subjective/subjective_988_base_r4_1.xlsx'
        dst_excel_path = f'{output_dir}/base.xlsx'
        os.system(f'cp {base_excel_path} {dst_excel_path}')


        fout = osp.join(output_dir, 'summary.csv')

        fout_flag = 0
        out_excel_path = osp.join(output_dir, 'summary.xlsx')



        results_folder = osp.join(work_dir, 'results')
        prediction_folder = osp.join(work_dir, 'predictions')

        for subdir in os.listdir(prediction_folder):
            if subdir not in self.eval_model_abbrs:
                continue
            
            model_abbr = subdir
            subdir_eval_path = os.path.join(results_folder, subdir) + '_judged-by--' + self.judge_abbr
            subdir_pred_path = os.path.join(prediction_folder, subdir)

            if os.path.isdir(subdir_eval_path):
                model = subdir
                for dataset in dataset_cfgs:
                    dataset_abbr = dataset_abbr_from_cfg(dataset)
                    eval_filepath = os.path.join(subdir_eval_path,
                                            dataset_abbr + '.json')
                    result = mmengine.load(eval_filepath)

                    pred_filepath = os.path.join(subdir_pred_path,
                                            dataset_abbr + '.json')
                    preds = mmengine.load(pred_filepath)


                    base_data = pd.read_excel(dst_excel_path)

                    # Load results
                    judged_answers = []
                    for k, v in result.items():
                        prediction = preds[k]['prediction']
                        rating, score = post_process_r4(v['prediction'])
                        question_id = v['gold']

                        # print('--------------------------')
                        # print(v['prediction'])
                        # print(rating)

                        row = base_data[base_data['序号'] == question_id]

                        # prevent illegal char in prediction
                        ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
                        prediction = ILLEGAL_CHARACTERS_RE.sub(r'', prediction)

                        base_data.loc[row.index, model_abbr] = prediction

                        if rating is not None: # and score != -1:
                            judged_answers.append({
                                'rating': rating,
                                'score': score
                            })

                            # write results to base dataframe
                            row = base_data[base_data['序号'] == question_id]
                            base_data.loc[row.index, '是否正确-模型'] = rating.get('正确性判断', None)
                            base_data.loc[row.index, '打分原因'] = v['prediction']


                            # base_data.loc[row.index, '正确性核查-模型-2'] = rating['正确性判断']
                        else:
                            print(f"---------index: {k}, Missing Keys: {{正确性打分}}-------------")
                            print(v['prediction'])

                    print(
                        f'Among {len(result)} judgements, successfully extracted {len(judged_answers)} judgements.'
                    )

                    # 初始化一个嵌套字典用于存储模型和评分
                    dimension_ratings = defaultdict(int)
                    dimension_counts = defaultdict(int)

                    for ans in judged_answers:
                        for k, v in ans['rating'].items():
                            if k == '正确性判断':
                                if v == '是': # ignore the -1
                                    dimension_ratings[k] += 1
                                dimension_counts[k] += 1

                    # average score
                    dimension_avg_ratings = defaultdict(float)
                    for dimension, total_score in dimension_ratings.items():
                        dimension_avg_ratings[
                            dimension] = total_score / dimension_counts[
                                dimension]

                    scores = {model: dimension_avg_ratings}

                    rows = list(scores.keys())
                    columns = list(scores[rows[0]].keys())
                    with open(fout, 'a+', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        if fout_flag == 0:
                            writer.writerow(['模型'] + columns)
                            fout_flag += 1
                        for row in rows:
                            writer.writerow(
                                [row] +
                                [scores[row][column] for column in columns])
                            
                    base_data.to_excel(out_excel_path)

    def summarize_csv(self,
                  time_str: str = datetime.now().strftime('%Y%m%d_%H%M%S')):
        """Summarize the subjectivity analysis based on evaluation results.

        Args:
            time_str (str): Timestamp for file naming.

        Returns:
            pd.DataFrame: The summary results.
        """
        dataset_cfgs = self.cfg['datasets']
        work_dir = self.cfg['work_dir']
        self.work_dir = work_dir

        self.time_str = time_str
        output_path = osp.join(self.work_dir, 'summary',
                               f'summary_{self.time_str}.txt')
        output_dir = osp.join(osp.split(output_path)[0], f'{self.time_str}')
        mmengine.mkdir_or_exist(output_dir)
        results_folder = osp.join(work_dir, 'results')
        fout = osp.join(output_dir, 'summary.csv')
        fout_flag = 0
        fout_details = osp.join(output_dir, 'summary_details.csv')
        fout_details_flag = 0

        for subdir in os.listdir(results_folder):
            if subdir not in self.eval_model_abbrs:
                continue
            subdir_path = os.path.join(results_folder, subdir)
            if os.path.isdir(subdir_path):
                model = subdir
                for dataset in dataset_cfgs:
                    dataset_abbr = dataset_abbr_from_cfg(dataset)
                    filepath = os.path.join(subdir_path,
                                            dataset_abbr + '.json')
                    result = mmengine.load(filepath)
                    judged_answers = []
                    references = []
                    for k, v in result.items():
                        rating, score = post_process(v['prediction'])
                        if rating is not None: # and score != -1:
                            judged_answers.append({
                                'rating': rating,
                                'score': score
                            })
                            references.append(v['gold'])
                        with open(fout_details, 'a+', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            if fout_details_flag == 0:
                                writer.writerow(rating.keys())
                                fout_details_flag += 1
                            writer.writerow(rating.values())
                    print(
                        f'Among {len(result)} judgements, successfully extracted {len(judged_answers)} judgements.'
                    )

                    # 初始化一个嵌套字典用于存储模型和评分
                    dimension_ratings = defaultdict(int)
                    dimension_counts = defaultdict(int)

                    for ans, ref in zip(judged_answers, references):
                        for k, v in ans['rating'].items():
                            if k != '综合得分':
                                if v != -1: # ignore the -1
                                    dimension_ratings[k] += v
                                    dimension_counts[k] += 1
                        dimension_ratings['综合得分'] += ans['score']
                        dimension_counts['综合得分'] += 1

                    dimension_avg_ratings = defaultdict(float)
                    for dimension, total_score in dimension_ratings.items():
                        dimension_avg_ratings[
                            dimension] = total_score / dimension_counts[
                                dimension]

                    scores = {model: dimension_avg_ratings}

                    rows = list(scores.keys())
                    columns = list(scores[rows[0]].keys())
                    with open(fout, 'a+', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        if fout_flag == 0:
                            writer.writerow(['模型'] + columns)
                            fout_flag += 1
                        for row in rows:
                            writer.writerow(
                                [row] +
                                [scores[row][column] for column in columns])


        with open(fout, 'r') as f:
            x = from_csv(f)
        print(x)


    
    def summarize(self,
                time_str: str = datetime.now().strftime('%Y%m%d_%H%M%S')):
        self.summarize_excel_r4(time_str)