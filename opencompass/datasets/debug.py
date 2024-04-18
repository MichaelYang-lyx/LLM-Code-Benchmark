import csv
import os.path as osp
import json

from datasets import Dataset

from opencompass.registry import LOAD_DATASET

from .base import BaseDataset


@LOAD_DATASET.register_module()
class DebugDatasetCSV(BaseDataset):

    @staticmethod
    def load(path: str, name: str):
        dataset = []
        filename = osp.join(path, f'{name}.csv')
        with open(filename, encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                item = dict(zip(header, row)) # make a dictionary
                dataset.append(item)
        return Dataset.from_list(dataset)

class DebugDatasetJSON(BaseDataset):
    @staticmethod
    def load(path: str):
        raw_data=[]
        with open(path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            for problem in json_data:
                question = problem['question']
                raw_data.append({
                    'question': f'{question}',
                })
        return Dataset.from_list(raw_data)