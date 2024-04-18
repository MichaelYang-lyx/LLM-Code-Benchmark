# flake8: noqa: E501
import csv
import os
import os.path as osp
import re
from collections import defaultdict
from datetime import datetime
import json
import glob

import mmengine
import numpy as np
from mmengine import ConfigDict
import pandas as pd

try:
    from prettytable import from_csv
except ImportError:
    from_csv = None

from opencompass.utils import dataset_abbr_from_cfg, model_abbr_from_cfg

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
                res[v['gold']['question_id']].update({
                    "judge_prompt": v['origin_prompt'],
                    "judgement": v['prediction'],
                    "round": v['gold']['others']['round']
                })

    return res



class SenseBenchMultiRoundSummarizer:
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

        # self.time_str = time_str
        # output_path = osp.join(self.work_dir, 'summary',
        #                        f'summary_{self.time_str}.txt')
        # output_dir = osp.join(osp.split(output_path)[0], f'{self.time_str}')
        # mmengine.mkdir_or_exist(output_dir)        

        results_folder = osp.join(work_dir, 'results')
        prediction_folder = osp.join(work_dir, 'predictions')
        summary_folder = osp.join(work_dir, 'summary')

        for subdir in os.listdir(prediction_folder):
            if subdir not in self.eval_model_abbrs:
                continue
            
            model_abbr = subdir
            subdir_eval_path = os.path.join(results_folder, subdir) + '_judged-by--' + self.judge_abbr
            subdir_pred_path = os.path.join(prediction_folder, subdir)
            subdir_summ_path = os.path.join(summary_folder, subdir) + '_judged-by--' + self.judge_abbr
            mmengine.mkdir_or_exist(subdir_summ_path)



            if os.path.isdir(subdir_eval_path):
                model = subdir
                for dataset in dataset_cfgs:
                    dataset_abbr = dataset_abbr_from_cfg(dataset)

                    # copy source excel to output path
                    dataset_excel_path = dataset['path'].replace('.json', '.xlsx')
                    base_data = pd.read_excel(dataset_excel_path)
                    out_excel_path = osp.join(subdir_summ_path, f'summary_{dataset_abbr}.xlsx')

                    summary = read_prediction_and_result(dataset_abbr, subdir_pred_path, subdir_eval_path)


                    max_round = 8  # depends on dataset
                    round_wrong_cnt = [0 for i in range(max_round)]
                    round_total_cnt = [0 for i in range(max_round)]


                    # Load results
                    judged_answers = []
                    for question_id, v in summary.items():
                        prediction = v['prediction']
                        rating = v['judgement']

                        wrong_preds_list, failed = self.post_process(rating)
                        num_wrong_preds = len(wrong_preds_list)
                        if not failed:
                            score = 1-num_wrong_preds/v['round']
                            judged_answers.append(score)
                        else:
                            score = ''
                            print('question_id: ', question_id)
                            print('judgement: ', rating)


                        for wr in wrong_preds_list:
                            round_wrong_cnt[int(wr)] += 1
                        
                        for tr in range(v['round']):
                            round_total_cnt[tr] += 1
                         
                        row = base_data[base_data['question_id'] == question_id]

                        # prevent illegal char in prediction
                        # ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
                        # prediction = ILLEGAL_CHARACTERS_RE.sub(r'', prediction)

                        base_data.loc[row.index, model_abbr] = str(prediction)

                        # only for generating reference answer
                        # pred_valid_json = prediction.replace("'", '"')
                        # pred_valid_json = pred_valid_json.replace("\n", "\\n")
                        # try:
                        #     prediction_json = json.loads(pred_valid_json)
                        # except:
                        #     print(pred_valid_json)
                        # for entry in prediction_json:
                        #     round = entry['round']
                        #     answer = entry['assistant']
                        #     base_data.loc[row.index, 'reference'+str(round)] = answer

                        
                        if rating is not None: # and score != -1:
                            # write results to base dataframe
                            row = base_data[base_data['question_id'] == question_id]
                            base_data.loc[row.index, 'judged-by-GPT4-detail'] = v['judgement']
                            base_data.loc[row.index, 'judged-by-GPT4-score'] = score
                            

                        else:
                            print(v['prediction'])

                    print(
                        f'Among {len(summary)} judgements, successfully extracted {len(judged_answers)} judgements.'
                    )
                            
                    base_data.to_excel(out_excel_path)
                
                    # print round acc
                    for round_i, (rw, rt) in enumerate(zip(round_wrong_cnt, round_total_cnt)):
                        if round_i == 0:
                            continue
                        print(f'round {round_i} acc is {1 - rw / rt}')
                    


    
    def post_process(self, text):
        """
        extract the failed answers from judgements. example text:
        输出：[6]
        原因：在第六轮对话中，assistant错误地回答了春天到来后勤劳工作的动物，只提到了蜜蜂，
        并未提到故事中的蝗虫在春天也改过自新，成为勤劳的蝗虫。这与用户提供的故事内容不符，
        因为故事明确提到蝗虫在蜜蜂的帮助下已经改变，且承诺春天到来后将自己寻找食物。
        """
        match = re.findall(r'\[(\d+(?:,?\s*\d+)*)\]', text)
        if match:
            numbers = match[0]
            number_list = numbers.split(',')
            number_list = [int(num.strip()) for num in number_list]
            return number_list, 0
        elif re.findall(r'输出：\[\]', text):
            return [], 0
        else:
            return [], 1        
        

    def summarize(self,
                time_str: str = datetime.now().strftime('%Y%m%d_%H%M%S')):
        self.summarize_excel(time_str)
