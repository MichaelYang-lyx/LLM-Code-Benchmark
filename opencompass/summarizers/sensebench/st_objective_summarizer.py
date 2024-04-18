# flake8: noqa: E501
import os
import re
import json
import glob
import mmengine
import os.path as osp
import numpy as np
import pandas as pd

from datetime import datetime
from mmengine import ConfigDict


from opencompass.utils import dataset_abbr_from_cfg


def extract_first_capital_letter(string):
    pattern = r'[A-Z]'
    match = re.search(pattern, string)
    if match:
        return match.group()
    else:
        return None

def post_process_select(prediction):
    format_pred = extract_first_capital_letter(prediction)

    failed_flag = 1 if format_pred is None else 0

    return format_pred, failed_flag


def post_process(dataset_abbr: str, prediction: str):
    pattern_score = r'ceval|cantonese_mmlu|st_cantonese_objective'
    
    if re.search(pattern_score, dataset_abbr, re.IGNORECASE):
        format_pred, status = post_process_select(prediction)
    else:
        raise NotImplementedError(f'un-support dataset postprocess: {dataset_abbr}')
    
    return format_pred, status


def read_prediction_and_result(dataset_abbr, pred_folder):
    
    res = {}

    json_paths = glob.glob(f'{pred_folder}/{dataset_abbr}*.json')
    for fn in json_paths:
        r = mmengine.load(fn)
        for k, v, in r.items():
            res[k] = {
                "prediction": v['prediction'],
                "gt": v['gold']
            }

    return res

def rating_YesNo(prediction, gt):
    score = 1 if prediction == gt else 0
    return score


def rating(dataset_abbr, prediction, gt):
    pattern_score = r'ceval|cantonese_mmlu|st_cantonese_objective'
    
    if re.search(pattern_score, dataset_abbr, re.IGNORECASE):
        score = rating_YesNo(prediction, gt)
    else:
        raise NotImplementedError(f'un-support dataset postprocess: {dataset_abbr}')
    
    return score


class STObjectiveSummarizer:
    """Do the subjectivity analyze based on evaluation results.

    Args:
        config (ConfigDict): The configuration object of the evaluation task.
            It's expected to be filled out at runtime.
    """

    def __init__(self, config: ConfigDict) -> None:
        self.tasks = []
        self.cfg = config

    def summarize_obj(self, time_str: str = datetime.now().strftime('%Y%m%d_%H%M%S')):
        dataset_cfgs = self.cfg['datasets']
        work_dir = self.cfg['work_dir']

        results_folder = osp.join(work_dir, 'results') 
        prediction_folder = osp.join(work_dir, 'predictions')
        summary_folder = osp.join(work_dir, 'summary')

        for subdir in os.listdir(prediction_folder):
            model_abbr = subdir
            subdir_pred_path = os.path.join(prediction_folder, subdir)
            subdir_summ_path = os.path.join(summary_folder, subdir)
            mmengine.mkdir_or_exist(subdir_summ_path)
            
            out_excel_path = osp.join(subdir_summ_path, f'summary_score_{time_str}.xlsx')
            

            if os.path.isdir(subdir_pred_path):
                average_scores = []
                dataset_abbrs = []
                for dataset in dataset_cfgs:
                    scores = []
                    dataset_abbr = dataset_abbr_from_cfg(dataset)
                    
                    # Load results
                    extract_failure_case = 0
                    summary = read_prediction_and_result(dataset_abbr,  subdir_pred_path)

                    for question_id, v in summary.items():
                        prediction = v['prediction']
                        gt = v['gt']

                        format_pred, status = post_process(dataset_abbr, prediction)

                        extract_failure_case += status

                        score = rating(dataset_abbr, format_pred, gt)
                        scores.append(score)

                    average_score = np.mean(scores)*100
                    dataset_abbrs.append(dataset_abbr)
                    average_scores.append(average_score)
                    print(
                       f'{dataset_abbr}:  Accuracy:{average_score:.2f}%, Among {len(summary)} judgements, {len(summary) - extract_failure_case} cases were successfully extracted.'
                    )

                # Save summary to excel
                dataset_abbrs.append('Total')
                average_scores.append(np.mean(average_scores))
                out_excel = pd.DataFrame({'Dataset': dataset_abbrs, 'Accuracy(%)': average_scores})
                out_excel.to_excel(out_excel_path, index=False)

    
    def summarize(self, time_str: str = datetime.now().strftime('%Y%m%d_%H%M%S')):
        self.summarize_obj(time_str)