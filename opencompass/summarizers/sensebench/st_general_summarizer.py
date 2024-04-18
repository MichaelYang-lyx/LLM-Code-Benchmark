# flake8: noqa: E501
import os
import re
import json
import glob
import mmengine

import numpy as np
import pandas as pd
import os.path as osp

from datetime import datetime
from mmengine import ConfigDict
from collections import defaultdict


try:
    from prettytable import from_csv
except ImportError:
    from_csv = None

from opencompass.utils import dataset_abbr_from_cfg, model_abbr_from_cfg


all_dimensions = [
    '事实正确性', '满足用户需求', '安全无害', '清晰度', '逻辑性', '完备性', '创造性', '可负责程度', '逻辑连贯性',
    '公平与可负责程度', '丰富度', '综合得分'
]

def remove_illegal_characters(text):
    # Define the pattern to match illegal characters
    pattern = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

    # Remove illegal characters from the text
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def add_color(text, color):
    '''
    add print color
    '''
    colors = {
        'red': '\033[1;31m',
        'green': '\033[1;32m',
        'yellow': '\033[1;33m',
        'blue': '\033[1;34m',
        'magenta': '\033[1;35m',
        'cyan': '\033[1;36m'
    }
    if color not in colors:
        return text
    return colors[color] + text + '\033[0m'


def post_process_YesNo(judgement, judge_model = 'GPT-4-Turbo'):

    def extract_rating(text):
        # pattern = r'{(.*?)}(?![^{]*{)'  # match last brackets - TODO \{[^{}]*\}$
        
        # pattern = r"\{([^\{\}]*)\}(?=[^\{\}]*$)"
        # match = re.findall(pattern, text)
        pattern = r"\{([^\{\}]*)\}"
        all_matches = re.findall(pattern, text)
        if all_matches:
            
            # 支持单引号和双引号
            #kv_pattern = r"'*\"*‘*“*([^\"']*)'*\"*’*”*:(.*)"
            kv_pattern = r"(.*):(.*)"
            kv_matches = [re.findall(kv_pattern, _str) for _str in all_matches]
            
            kv_matches = [ _match for _match in kv_matches if _match]
         
            # 目前是取第一个匹配的结果，后面可能会用到多个匹配结果
            result_dict = {key.strip("' \"‘’“”"): value.strip("' \"‘’“”") for key, value in kv_matches[0]}
            return result_dict
        else:
            return None

    format_evaluation = {}
    format_evaluation['打分原因'] = judgement

    judgement = judgement.replace('\n', '')
    rating = extract_rating(judgement)

    failed_flag = 0

    if rating is not None:
        format_evaluation[f'是否正确-by-{judge_model}'] = rating.get('正确性判断', None)
    else:
        failed_flag = 1

    return format_evaluation, failed_flag

def post_process_fc(prediction):
    format_evaluation = {}
    failed_flag = 0

    # print(prediction)
    pattern = r'{.*}'
    tool_call_str = re.search(pattern, prediction)
    if tool_call_str:
        json_str = tool_call_str.group(0)
        try:
            tool_call = json.loads(json_str)
            tool_call = tool_call['name']
            format_evaluation['tool_call_result'] = tool_call
        except:
            pass
    else:
        format_evaluation['tool_call_result'] = prediction
        format_evaluation['place-holder'] = "" # for sensearena
        
    return format_evaluation, failed_flag

def post_process_score(judgement, judge_model = 'GPT-4-Turbo'):
    format_evaluation = {}
    failed_flag = 0

    score_regex = r'"分数":\s*([^,]+)'
    reason_regex = r'"原因":\s*"([^"]+)"'

    score_match = re.search(score_regex, judgement)
    reason_match = re.search(reason_regex, judgement)

    if score_match and reason_match:
        score = score_match.group(1)
        reason = reason_match.group(1)

        format_evaluation['原因'] = remove_illegal_characters(reason)
        format_evaluation[f'打分-by-{judge_model}'] = score
    else:
        format_evaluation['原因'] = '未找到原因'
        format_evaluation[f'打分-by-{judge_model}'] = 0
        failed_flag = 1

    return format_evaluation, failed_flag


def post_process(prediction: str, judgement: str, dataset_abbr: str, judge_model: str = 'GPT-4-Turbo'):
    '''
    process judgement into dict that can be written to Excel according to dataset_abbr
    e.g:
    judgement -> {
        "正确性判断": 是,
        "分数: 9,
        "原因": xxxxxx
        ...
        ...
    }
    '''

    pattern_YesNo = r'instruction_following|knowledge|math_and_logic|summary_and_retrieve|st988'
    pattern_score = r'human_like_chatting|writing|scenarios_cantonese'
    pattern_passby = r'functioncall'
    
    if re.search(pattern_YesNo, dataset_abbr, re.IGNORECASE):
        format_evaluation, status = post_process_YesNo(judgement, judge_model)
    elif re.search(pattern_score, dataset_abbr, re.IGNORECASE):
        format_evaluation, status = post_process_score(judgement, judge_model)
    elif re.search(pattern_passby, dataset_abbr, re.IGNORECASE):
        format_evaluation, status = post_process_fc(prediction)
    else:
        raise NotImplementedError(f'un-support dataset postprocess: {dataset_abbr}')
    
    return format_evaluation, status


def calc_score(base_data, dataset_abbr):
    pattern_YesNo = r'instruction_following|knowledge|math_and_logic|summary_and_retrieve|st988'
    pattern_score = r'human_like_chatting|writing|scenarios_cantonese'
    pattern_fc = r'functioncall'
    
    total_rows = len(base_data)

    if re.search(pattern_YesNo, dataset_abbr, re.IGNORECASE):
        score = base_data.iloc[:, -1].dropna().value_counts()['是'] / total_rows * 100
    elif re.search(pattern_score, dataset_abbr, re.IGNORECASE):
        base_data.iloc[:,-1] = pd.to_numeric(base_data.iloc[:,-1], errors='coerce')
        score = base_data.iloc[:, -1].dropna().mean() * 20
    elif re.search(pattern_fc, dataset_abbr, re.IGNORECASE):
        count_condition = (base_data.iloc[:, -2] == base_data.iloc[:, 3]).sum()
        score = count_condition / total_rows * 100
    else:
        raise NotImplementedError(f'un-support calc_score: {dataset_abbr}')
    
    return score





def read_prediction_and_result(dataset_abbr, pred_folder, results_folder):
    res = {}

    json_paths = glob.glob(f'{pred_folder}/{dataset_abbr}*.json')
    for fn in json_paths:
        r = mmengine.load(fn)
        for k, v, in r.items():
            res[v['gold']] = {
                "origin_prompt": v['origin_prompt'],
                "prediction": v['prediction']
            }

    json_paths = glob.glob(f'{results_folder}/{dataset_abbr}*.json')
    if json_paths:  # json_paths might be empty at functioncall
        for fn in json_paths:
            r = mmengine.load(fn)
            for k, v in r.items():
                res[v['gold']].update({
                    "judge_prompt": v['origin_prompt'],
                    "judgement": v['prediction']
                })

    return res


class STCapabilityGeneralSummarizer:
    """Do the subjectivity analyze based on evaluation results.

    Args:
        config (ConfigDict): The configuration object of the evaluation task.
            It's expected to be filled out at runtime.
    """

    def __init__(self, config: ConfigDict) -> None:
        self.tasks = []
        self.cfg = config
        try:
            self.judge_abbr = model_abbr_from_cfg(self.cfg['judge_model'])
        except:
            self.judge_abbr = ""

    def summarize_excel_r4(self, time_str: str = datetime.now().strftime('%Y%m%d_%H%M%S')):
        dataset_cfgs = self.cfg['datasets']
        work_dir = self.cfg['work_dir']
        self.work_dir = work_dir

        results_folder = osp.join(work_dir, 'results') 
        prediction_folder = osp.join(work_dir, 'predictions')
        summary_folder = osp.join(work_dir, 'summary')

        for subdir in os.listdir(prediction_folder):
            model_abbr = subdir
            subdir_eval_path = os.path.join(results_folder, subdir) + '_judged-by--' + self.judge_abbr
            subdir_pred_path = os.path.join(prediction_folder, subdir)
            subdir_summ_path = os.path.join(summary_folder, subdir)
            mmengine.mkdir_or_exist(subdir_summ_path)

            if os.path.isdir(subdir_pred_path):

                model = subdir
                for dataset in dataset_cfgs:
                    dataset_abbr = dataset_abbr_from_cfg(dataset)
                    
                    dataset_excel_path = dataset['path'].replace('json', 'xlsx')
                    base_data = pd.read_excel(dataset_excel_path)
                    out_excel_path = osp.join(subdir_summ_path, f'summary_{dataset_abbr}.xlsx')

                    # Load results
                    extract_failure_case = 0
                    summary = read_prediction_and_result(dataset_abbr, subdir_pred_path, subdir_eval_path)

                    for question_id, v in summary.items():
                        prediction = v['prediction'].replace('\b', '')
                        judgement = v.get('judgement', "")

                        format_evaluation, status = post_process(prediction, judgement, dataset_abbr, self.judge_abbr)
                        row = base_data[base_data['question_id'] == question_id]
                        base_data.loc[row.index, model_abbr] = prediction

                        extract_failure_case += status
                        
                        # excel 的格式需要是 prediction, judgement, score
                        for k, v in format_evaluation.items():
                            base_data.loc[row.index, k] = v

                    base_data.to_excel(out_excel_path)
                    
                    ## 取最后一列算分
                    score = calc_score(base_data, dataset_abbr)

                    print(
                       f'{dataset_abbr}:  {len(summary) - extract_failure_case}/{len(summary)} cases were successfully extracted. The score is {score:.2f}.'
                    )



    def summarize(self,
                  time_str: str = datetime.now().strftime('%Y%m%d_%H%M%S')):
        self.summarize_excel_r4(time_str)