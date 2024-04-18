# flake8: noqa: E501
import csv
import os
import os.path as osp
import re
from collections import defaultdict
from datetime import datetime
from itertools import product
import pandas as pd

import mmengine
from mmengine import ConfigDict

try:
    from prettytable import from_csv
except ImportError:
    from_csv = None

from opencompass.partitioners.sub_naive import remove_duplicate_pairs
from opencompass.utils import dataset_abbr_from_cfg, model_abbr_from_cfg


def match_general_answer(s):
    temp = s[0]
    if temp in ['A', 'B', 'C', 'D']:
        return temp
    else:
        return None


def match_GPT4_answer(s):
    if result := re.findall('(?:选择：|Choice: )([ABCD])', s):
        return result[0]
    else:
        return None


judge_map = {'smart': match_GPT4_answer, 'other': match_general_answer}


def call_function(name, arg):
    if name in judge_map:
        return judge_map[name](arg)
    else:
        print('Function not found in the map.')


class Corev2Summarizer:
    """Do the subjectivity analyze based on evaluation results.

    Args:
        config (ConfigDict): The configuration object of the evaluation task.
            It's expected to be filled out at runtime.
    """

    def __init__(self, config: ConfigDict, match_method='smart') -> None:
        self.tasks = []
        self.cfg = config
        self.match_method = match_method
        self.base_models = self.cfg['eval']['partitioner']['base_models']
        self.compare_models = self.cfg['eval']['partitioner']['compare_models']
        self.judge_abbr = model_abbr_from_cfg(self.cfg['judge_model'])

    def summarize(self,
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

        model_combinations = list(
            product(self.base_models, self.compare_models))
        unique_combinations = remove_duplicate_pairs(
            [combo for combo in model_combinations if combo[0] != combo[1]])

        for model_pair in unique_combinations:
            model1, model2, judge_model = model_pair[0]['abbr'], model_pair[1][
                'abbr'], self.judge_abbr
            subdir = model1 + '_' + model2 + '_judged-by--' + self.judge_abbr
            subdir_path = os.path.join(results_folder, subdir)
            if os.path.isdir(subdir_path):
                fout = osp.join(output_dir,
                                'judged-by--' + judge_model + '-report.csv')
                for dataset in dataset_cfgs:
                    dataset_abbr = dataset_abbr_from_cfg(dataset)
                    filename = os.path.join(subdir_path,
                                            dataset_abbr + '.json')
                    partial_filename = os.path.join(subdir_path,
                                                    dataset_abbr + '_0.json')
                    if osp.exists(osp.realpath(filename)):
                        result = mmengine.load(filename)
                    elif osp.exists(osp.realpath(partial_filename)):
                        filename = partial_filename
                        result = {}
                        i = 1
                        partial_dict_flag = 0
                        while osp.exists(osp.realpath(filename)):
                            res = mmengine.load(filename)
                            for k, v in res.items():
                                result[partial_dict_flag] = v
                                partial_dict_flag += 1
                            filename = os.path.join(
                                subdir_path,
                                dataset_abbr + '_' + str(i) + '.json')
                            i += 1
                    else:
                        result = {}

                    if len(result) == 0:
                        print('*' * 100)
                        print('There are no results for ' + filename + ' or ' +
                              partial_filename)
                        print('*' * 100)
                        assert len(result) > 0

                    judged_answers = []
                    references = []
                    for k, v in result.items():
                        judged_answers.append(
                            call_function(self.match_method, v['prediction']))
                        references.append(v['gold'])
                    successful_judged_answers = len(
                        judged_answers) - judged_answers.count(None)
                    print(
                        f'Among {len(judged_answers)} judgements, successfully extracted {successful_judged_answers} judgements.'
                    )
                    if successful_judged_answers == 0:
                        print('*' * 100)
                        print(
                            'There are no extracted judgements, please change your judge model or check your prompt!!!'
                        )
                        print('*' * 100)
                    assert successful_judged_answers > 0

                    win_both_model1, win_both_model2, half_draw_model1, half_draw_model2, categories = defaultdict(
                        float), defaultdict(float), defaultdict(
                            float), defaultdict(float), defaultdict(float)
                    model1 = references[0]['answer1']
                    model2 = references[0]['answer2']
                    for prediction, reference in zip(judged_answers,
                                                     references):
                        if prediction is not None:
                            categories[reference['capability'].split('-')
                                       [0]] += 1
                            categories[reference['capability']] += 1
                            winner = ''
                            if prediction == 'A':
                                winner = reference['answer1']
                            elif prediction == 'B':
                                winner = reference['answer2']
                            elif prediction == 'C':
                                win_both_model1[reference['capability'].split(
                                    '-')[0]] += 1
                                win_both_model2[reference['capability'].split(
                                    '-')[0]] += 1
                                win_both_model1[reference['capability']] += 1
                                win_both_model2[reference['capability']] += 1
                            if model1 == winner:
                                half_draw_model1[reference['capability'].split(
                                    '-')[0]] += 1
                                win_both_model1[reference['capability'].split(
                                    '-')[0]] += 1
                                half_draw_model1[reference['capability']] += 1
                                win_both_model1[reference['capability']] += 1
                            elif model2 == winner:
                                half_draw_model2[reference['capability'].split(
                                    '-')[0]] += 1
                                win_both_model2[reference['capability'].split(
                                    '-')[0]] += 1
                                half_draw_model2[reference['capability']] += 1
                                win_both_model2[reference['capability']] += 1
                    for capability in categories:
                        if capability not in half_draw_model1:
                            win_both_model1[capability] = 0.0
                            half_draw_model1[capability] = 0.0
                        else:
                            win_both_model1[capability] = round(
                                (win_both_model1[capability] /
                                 categories[capability]) * 100, 2)
                            half_draw_model1[capability] = round(
                                (half_draw_model1[capability] /
                                 categories[capability]) * 100, 2)
                        if capability not in half_draw_model2:
                            win_both_model2[capability] = 0.0
                            half_draw_model2[capability] = 0.0
                        else:
                            win_both_model2[capability] = round(
                                (win_both_model2[capability] /
                                 categories[capability]) * 100, 2)
                            half_draw_model2[capability] = round(
                                (half_draw_model2[capability] /
                                 categories[capability]) * 100, 2)
                    scores = {
                        'win_both_' + model1: win_both_model1,
                        'half_draw_' + model1: half_draw_model1,
                        'win_both_' + model2: win_both_model2,
                        'half_draw_' + model2: half_draw_model2
                    }
                    rows = list(scores.keys())
                    columns = list(scores[rows[0]].keys())
                    with open(fout, 'a+', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([model1 + '_vs_' + model2] + columns)
                        for row in rows:
                            writer.writerow(
                                [row] +
                                [scores[row][column] for column in columns])
            else:
                print(subdir_path + ' is not exist! please check!')
        with open(fout, 'r') as f:
            x = from_csv(f)
        print(x)



class Corev2SummarizerExcel:
    """Do the subjectivity analyze based on evaluation results.

    Args:
        config (ConfigDict): The configuration object of the evaluation task.
            It's expected to be filled out at runtime.
    """

    def __init__(self, config: ConfigDict, match_method='smart') -> None:
        self.tasks = []
        self.cfg = config
        self.match_method = match_method
        self.base_models = self.cfg['eval']['partitioner']['base_models']
        self.compare_models = self.cfg['eval']['partitioner']['compare_models']
        self.judge_abbr = model_abbr_from_cfg(self.cfg['judge_model'])

    def summarize(self,
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
        output_dir = osp.join(osp.split(output_path)[0])
        mmengine.mkdir_or_exist(output_dir)
        results_folder = osp.join(work_dir, 'results')
        

        model_combinations = list(
            product(self.base_models, self.compare_models))
        unique_combinations = remove_duplicate_pairs(
            [combo for combo in model_combinations if combo[0] != combo[1]])

        for model_pair in unique_combinations:
            model1, model2, judge_model = model_pair[0]['abbr'], model_pair[1][
                'abbr'], self.judge_abbr
            subdir = model1 + '_' + model2 + '_judged-by--' + self.judge_abbr
            subdir_path = os.path.join(results_folder, subdir)
            out_excel_path = osp.join(output_dir, 'summary_'+model1+'_vs_'+model2+'.xlsx')
            model1_prediction_path = osp.join(self.work_dir, 'predictions', model1)
            model2_prediction_path = osp.join(self.work_dir, 'predictions', model2)

            if os.path.isdir(subdir_path):
                fout = osp.join(output_dir,
                                'judged-by--' + judge_model + '-report.csv')
                for dataset in dataset_cfgs:
                    dataset_abbr = dataset_abbr_from_cfg(dataset)
                    filename = os.path.join(subdir_path,
                                            dataset_abbr + '.json')
                    partial_filename = os.path.join(subdir_path,
                                                    dataset_abbr + '_0.json')
                    filename_model1_prediction = os.path.join(model1_prediction_path,
                                            dataset_abbr + '.json')
                    filename_model2_prediction = os.path.join(model2_prediction_path,
                                            dataset_abbr + '.json')

                    if osp.exists(osp.realpath(filename)):
                        result = mmengine.load(filename)
                        model1_pred = mmengine.load(filename_model1_prediction)
                        model2_pred = mmengine.load(filename_model2_prediction)

                    elif osp.exists(osp.realpath(partial_filename)):
                        filename = partial_filename
                        result = {}
                        i = 1
                        partial_dict_flag = 0
                        while osp.exists(osp.realpath(filename)):
                            res = mmengine.load(filename)                       

                            for k, v in res.items():
                                result[partial_dict_flag] = v
                                partial_dict_flag += 1
                            filename = os.path.join(
                                subdir_path,
                                dataset_abbr + '_' + str(i) + '.json')
                            i += 1
                    else:
                        result = {}



                    if len(result) == 0:
                        print('*' * 100)
                        print('There are no results for ' + filename + ' or ' +
                              partial_filename)
                        print('*' * 100)
                        assert len(result > 0)
                                        
                    # cp base excel to summary folder
                    base_excel_path = result['0']['gold']['excel_path']
                    dst_excel_path = f'{output_dir}/base.xlsx'
                    os.system(f'cp {base_excel_path} {dst_excel_path}')
                    base_data = pd.read_excel(dst_excel_path)


                    judged_answers = []
                    references = []
                    for k, v in result.items():
                        judged_answer = call_function(self.match_method, v['prediction'])
                        judged_answers.append(judged_answer)
                        references.append(v['gold'])
                        
                        row = base_data[base_data['question_id'] == v['gold']['question_id']]
                        # prevent illegal char in prediction
                        ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
                        prediction = ILLEGAL_CHARACTERS_RE.sub(r'', v['prediction'])
                        
                        for idx, val in model1_pred.items():
                            if v['gold']['question_id']==val['gold']['question_id']:
                                model1_matched_idx = idx

                        for idx, val in model2_pred.items():
                            if v['gold']['question_id']==val['gold']['question_id']:
                                model2_matched_idx = idx
                        

                        model1_prediction = ILLEGAL_CHARACTERS_RE.sub(r'', model1_pred[model1_matched_idx]['prediction'])
                        model2_prediction = ILLEGAL_CHARACTERS_RE.sub(r'', model2_pred[model2_matched_idx]['prediction'])
                   
                        base_data.loc[row.index, model1+'_prediction'] = model1_prediction
                        base_data.loc[row.index, model2+'_prediction'] = model2_prediction

                        if model1 == v['gold']['answer1']:
                            order_switched = 0
                        else:
                            order_switched = 1

                        base_data.loc[row.index, 'switch_order'] = order_switched
                        base_data.loc[row.index, 'reason'] = v['prediction']

                        if judged_answer == 'A':
                            if order_switched==0:
                                base_data.loc[row.index, 'judge'] = 'A'
                            else:
                                base_data.loc[row.index, 'judge'] = 'B'
                            base_data.loc[row.index, v['gold']['answer1']] = 1
                            base_data.loc[row.index, v['gold']['answer2']] = 0
                        elif judged_answer == 'B':
                            if order_switched==0:
                                base_data.loc[row.index, 'judge'] = 'B'
                            else:
                                base_data.loc[row.index, 'judge'] = 'A'
                            base_data.loc[row.index, v['gold']['answer1']] = 0
                            base_data.loc[row.index, v['gold']['answer2']] = 1
                        elif judged_answer == 'C':
                            base_data.loc[row.index, 'judge'] = 'C'
                            base_data.loc[row.index, v['gold']['answer1']] = 1
                            base_data.loc[row.index, v['gold']['answer2']] = 1
                        elif judged_answer == 'D':
                            base_data.loc[row.index, 'judge'] = 'D'
                            base_data.loc[row.index, v['gold']['answer1']] = 0
                            base_data.loc[row.index, v['gold']['answer2']] = 0

                    successful_judged_answers = len(
                        judged_answers) - judged_answers.count(None)


                    print(
                        f'Among {len(judged_answers)} judgements, successfully extracted {successful_judged_answers} judgements.'
                    )
                    if successful_judged_answers == 0:
                        print('*' * 100)
                        print(
                            'There are no extracted judgements, please change your judge model or check your prompt!!!'
                        )
                        print('*' * 100)

                    assert successful_judged_answers > 0

                    win_both_model1, win_both_model2, half_draw_model1, half_draw_model2, categories = defaultdict(
                        float), defaultdict(float), defaultdict(
                            float), defaultdict(float), defaultdict(float)
                    model1 = references[0]['answer1']
                    model2 = references[0]['answer2']
                    for prediction, reference in zip(judged_answers,
                                                     references):
                        if prediction is not None:
                            categories[reference['capability'].split('-')
                                       [0]] += 1
                            categories[reference['capability']] += 1
                            winner = ''
                            if prediction == 'A':
                                winner = reference['answer1']
                            elif prediction == 'B':
                                winner = reference['answer2']
                            elif prediction == 'C':
                                win_both_model1[reference['capability'].split(
                                    '-')[0]] += 1
                                win_both_model2[reference['capability'].split(
                                    '-')[0]] += 1
                                win_both_model1[reference['capability']] += 1
                                win_both_model2[reference['capability']] += 1
                            if model1 == winner:
                                half_draw_model1[reference['capability'].split(
                                    '-')[0]] += 1
                                win_both_model1[reference['capability'].split(
                                    '-')[0]] += 1
                                half_draw_model1[reference['capability']] += 1
                                win_both_model1[reference['capability']] += 1
                            elif model2 == winner:
                                half_draw_model2[reference['capability'].split(
                                    '-')[0]] += 1
                                win_both_model2[reference['capability'].split(
                                    '-')[0]] += 1
                                half_draw_model2[reference['capability']] += 1
                                win_both_model2[reference['capability']] += 1
                    for capability in categories:
                        if capability not in half_draw_model1:
                            win_both_model1[capability] = 0.0
                            half_draw_model1[capability] = 0.0
                        else:
                            win_both_model1[capability] = round(
                                (win_both_model1[capability] /
                                 categories[capability]) * 100, 2)
                            half_draw_model1[capability] = round(
                                (half_draw_model1[capability] /
                                 categories[capability]) * 100, 2)
                        if capability not in half_draw_model2:
                            win_both_model2[capability] = 0.0
                            half_draw_model2[capability] = 0.0
                        else:
                            win_both_model2[capability] = round(
                                (win_both_model2[capability] /
                                 categories[capability]) * 100, 2)
                            half_draw_model2[capability] = round(
                                (half_draw_model2[capability] /
                                 categories[capability]) * 100, 2)
                    scores = {
                        'win_both_' + model1: win_both_model1,
                        'half_draw_' + model1: half_draw_model1,
                        'win_both_' + model2: win_both_model2,
                        'half_draw_' + model2: half_draw_model2
                    }
                    rows = list(scores.keys())
                    columns = list(scores[rows[0]].keys())
                    with open(fout, 'a+', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([model1 + '_vs_' + model2] + columns)
                        for row in rows:
                            writer.writerow(
                                [row] +
                                [scores[row][column] for column in columns])
                    
                    base_data.to_excel(out_excel_path)
            else:
                print(subdir_path + ' is not exist! please check!')
        with open(fout, 'r') as f:
            x = from_csv(f)
        print(x)
