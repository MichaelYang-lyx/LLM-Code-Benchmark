import json
import os

from datasets import Dataset, DatasetDict

from opencompass.openicl import BaseEvaluator
from opencompass.registry import LOAD_DATASET, TEXT_POSTPROCESSORS

from .base import BaseDataset
import re

@LOAD_DATASET.register_module()
class CantoneseObjDataset(BaseDataset):
    def load(self,path):
        dataset = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = json.loads(line.strip())
                dataset.append(line)
        return Dataset.from_list(dataset)


class CantoneseObjEvaluator(BaseEvaluator):

    def score(self, predictions, references):
        if len(predictions) != len(references):
            return {
                'error': 'predictions and references have different '
                'length'
            }
        correct = 0
        count = 0
        details = []
        for i, j in zip(predictions, references):
            detail = {'pred': i, 'answer': j, 'correct': False}
            count += 1
            if i == j:
                correct += 1
                detail['correct'] = True
            details.append(detail)
        result = {'accuracy': 100 * correct / count, 'details': details}
        return result

@TEXT_POSTPROCESSORS.register_module('cantonese_obj_postprocessor')
def cantonese_obj_postprocess(text):
    # 使用正则表达式查找所有的数字，包括浮点数
    numbers = re.findall(r'\d+\.\d+|\d+', text)
    
    # 如果没有找到任何数字，返回 None
    if not numbers:
        return 0

    ret = numbers[-1]
    # print(f'get ####{ret} from {text}')
    # print('----------------------------')

    return ret