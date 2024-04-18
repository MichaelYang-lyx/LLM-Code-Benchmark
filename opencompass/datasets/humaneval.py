import json
import os.path as osp
import re
import tempfile
from typing import List

from datasets import Dataset

from opencompass.openicl.icl_evaluator import BaseEvaluator
from opencompass.registry import LOAD_DATASET

from .base import BaseDataset


IMPORT_HELPER = {
    "python": [
        "import math",
        "import re",
        "import sys",
        "import copy",
        "import datetime",
        "import itertools",
        "import collections",
        "import heapq",
        "import functools",
        "import hashlib",
        "import numpy",
        "import numpy as np",
        "import string",
        "from typing import *",
        "from collections import *",
        "from functools import *"
    ],
    "go"   : [
        "math",
        "strings",
        "fmt",
        "strconv",
        "time",
        "bytes",
        "regexp",
        "sort",
        "math/rand",
        "crypto/md5",
    ],
    "cpp"   : [
        "#include<stdlib.h>",
        "#include<algorithm>",
        "#include<math.h>",
        "#include<stdio.h>",
        "#include<vector>",
        "#include<string>",
        "#include<climits>",
        "#include<cstring>",
        "#include<iostream>",
    ],
}

@LOAD_DATASET.register_module()
class HumanevalDataset(BaseDataset):
    @staticmethod
    def load(path: str, num_repeats: int = 1):
        """Load humaneval dataset for pass k mode.

        Note that you can use num_repeats > 1 when your model does not support
        `num_return_sequence` in generation, otherwise use the raw
        humaneval dataset and set `num_return_sequence` in model config to
        generate multiple responses for testing pass@k>1.

        It better to change your dataset abbr correspondingly if you want to
        change num_repeats>1, otherwise the number in
        `.cache/dataset_size.json` might be inconsistent.

        Args:
            num_repeats(int): Number of repetition for this dataset to get
        multiple responses in special cases.
        """
        dataset = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                dataset.extend(
                    [json.loads(line.strip()) for _ in range(num_repeats)])
        return Dataset.from_list(dataset)


class HumanEvaluator(BaseEvaluator):
    """Evaluator for HumanEval or EvalPlus."""

    def __init__(self,
                 k: List[int] = [1, 10, 100],
                 metric: str = 'HumanEval') -> None:
        self.metric = metric
        assert self.metric in ['HumanEval', 'EvalPlus', 'LeetCode']
        if self.metric == 'HumanEval':
            try:
                from human_eval.data import HUMAN_EVAL, write_jsonl
                from human_eval.evaluation import \
                    evaluate_functional_correctness
                self.write_jsonl = write_jsonl
                self.HUMAN_EVAL = HUMAN_EVAL
                self.eval = evaluate_functional_correctness
            except ImportError:
                raise ImportError(
                    'Please install human_eval use following steps:\n'
                    'git clone git@github.com:open-compass/human-eval.git\n'
                    'cd human-eval && pip install -e .')
        elif self.metric == 'HumanEvalx':
            from human_eval.data import HUMAN_EVAL
            from sense_eval.data import write_jsonl, read_problems
            from sense_eval.evaluation import \
                evaluate_functional_correctness
            self.write_jsonl = write_jsonl
            self.HUMAN_EVAL = HUMAN_EVAL
            self.eval = evaluate_functional_correctness
            self.read_problems = read_problems
        elif self.metric == 'EvalPlus':
            try:
                from evalplus.data import write_jsonl
                from evalplus.evaluate import evaluate
                self.write_jsonl = write_jsonl
                self.eval = evaluate
            except ImportError:
                raise ImportError(
                    'Please install evalplus use following steps:\n'
                    'git clone --recurse-submodules git@github.com:open-compass/human-eval.git\n'  # noqa
                    'cd human-eval\n'
                    'pip install -e .\n'
                    'pip install -e evalplus\n')
        elif self.metric == 'LeetCode':
            import os
            try:
                # import sys
                # sys.path.append('/data/LLM/code/sense-eval')
                from sense_eval.data import write_jsonl, read_problems
                from sense_eval.evaluation import \
                    evaluate_functional_correctness
                self.write_jsonl = write_jsonl
                self.LEETCODE_FILE = './data/leetcode/leetcode-20240121-Jul.jsonl'
                self.eval = evaluate_functional_correctness
                self.read_problems = read_problems
            except ImportError:
                raise ImportError(
                    'please install sense-eval')

        self.k = k
        super().__init__()

    def score(self, predictions, references, test_set):
        prompts = [item['prompt'] for item in test_set]
        humaneval_preds = []
        if self.metric == 'HumanEval':
            # create json file in human_eval format
            for preds, refer in zip(predictions, references):
                # suits for two case
                # 1. use repeated dataset
                # 2. use `num_return_sequences` to generate multiple responses
                if not isinstance(preds, list):
                    preds = [preds]
                for pred in preds:
                    humaneval_preds.append({
                        'task_id': refer,
                        'completion': pred
                    })
            with tempfile.TemporaryDirectory() as tmp_dir:
                out_dir = osp.join(tmp_dir, 'human_eval.json')
                self.write_jsonl(out_dir, humaneval_preds)
                score = self.eval(out_dir,
                                  self.k,
                                  n_workers=4,
                                  timeout=3.0,
                                  problem_file=self.HUMAN_EVAL,
                                  ignore_incomplete=True)
                return {f'humaneval_{k}': score[k] * 100 for k in score}
        elif self.metric == 'HumanEvalx':
            # create json file in human_eval format
            # solution should be setup + completion + test_case
            problems = self.read_problems(self.HUMAN_EVAL)
            test_setup = "\n".join(IMPORT_HELPER["python"]) + "\n"
            for preds, task_id in zip(predictions, references):
                test_case = problems[task_id]['test']
                entry_point = problems[task_id]['entry_point']
                solution = test_setup + preds + "\n" + test_case + f"check({entry_point})"

                if not isinstance(preds, list):
                    preds = [solution]

                for pred in preds:
                    humaneval_preds.append({
                        'task_id': task_id,
                        'solution': pred
                    })

            with tempfile.TemporaryDirectory() as tmp_dir:
                out_dir = osp.join(tmp_dir, 'leet_code.json')
                self.write_jsonl(out_dir, humaneval_preds)
                score = self.eval(out_dir,
                                  self.k,
                                  n_workers=4,
                                  timeout=3.0)
                return {f'humaneval_{k}': score[k] * 100 for k in score}

        elif self.metric == 'EvalPlus':
            for preds, refer, prompt in zip(predictions, references, prompts):
                if not isinstance(preds, list):
                    preds = [preds]
                for pred in preds:
                    humaneval_preds.append({
                        'task_id': refer,
                        'solution': prompt + pred
                    })
            with tempfile.TemporaryDirectory() as tmp_dir:
                out_dir = osp.join(tmp_dir, 'human_eval.jsonl')
                self.write_jsonl(out_dir, humaneval_preds)
                flags = dict(dataset='humaneval',
                             samples=out_dir,
                             base_only=None,
                             parallel=None,
                             i_just_wanna_run=None,
                             test_details=0.2,
                             min_time_limit=0.2,
                             gt_time_limit_factor=4.0,
                             mini=None)
                score = self.eval(flags)
                return {f'humaneval_plus_{k}': score[k] * 100 for k in score}
        elif self.metric == 'LeetCode':
            # create json file in human_eval format
            # solution should be setup + completion + test_case
            problems = self.read_problems(self.LEETCODE_FILE)
            test_setup = "\n".join(IMPORT_HELPER["python"]) + "\n"
            for preds, task_id in zip(predictions, references):
                test_case = problems[task_id]['test']
                solution = test_setup + preds + "\n" + test_case

                if not isinstance(preds, list):
                    preds = [solution]

                for pred in preds:
                    humaneval_preds.append({
                        'task_id': task_id,
                        'solution': pred
                    })

            with tempfile.TemporaryDirectory() as tmp_dir:
                out_dir = osp.join(tmp_dir, 'leet_code.json')
                self.write_jsonl(out_dir, humaneval_preds)
                score = self.eval(out_dir,
                                  self.k,
                                  n_workers=4,
                                  timeout=3.0)
                return {f'humaneval_{k}': score[k] * 100 for k in score}




def humaneval_postprocess(text: str) -> str:
    if '```' in text:
        blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
        if len(blocks) == 0:
            text = text.split('```')[1]  # fall back to default strategy
        else:
            text = blocks[0]  # fetch the first code block
            if not text.startswith('\n'):  # in case starting with ```python
                text = text[max(text.find('\n') + 1, 0):]
    if text.strip().startswith('from') or text.strip().startswith('import'):
        def_idx = text.find('def')
        if def_idx != -1:
            text = text[max(text.find('\n', def_idx) + 1, 0):]
    text = text.split('\n\n')[0]
    text = text.lstrip('\n')
    if text.strip().startswith('def'):
        text = '\n'.join(text.split('\n')[1:])
    if not text.startswith('    '):
        if text.startswith(' '):
            text = '    ' + text.lstrip()
        else:
            text = '\n'.join(['    ' + line for line in text.split('\n')])
    return text


def humaneval_postprocess_v2(text: str) -> str:
    """This is an advanced version of previous postprocess to handle more
    situations, better to use this one."""
    try:
        # for chatGLM related text
        eval_text = eval(text)
    except Exception:
        pass
    else:
        if isinstance(eval_text, str):
            text = eval_text
    text = text.lstrip('\n')
    if '```' in text:
        blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
        if len(blocks) == 0:
            text = text.split('```')[1]  # fall back to default strategy
        else:
            text = blocks[0]  # fetch the first code block
            if not text.startswith('\n'):  # in case starting with ```python
                text = text[max(text.find('\n') + 1, 0):]
    if text.strip().startswith('from') or text.strip().startswith('import'):
        def_idx = text.find('def')
        if def_idx != -1:
            text = text[max(text.find('\n', def_idx) + 1, 0):]
    # remove empty lines
    text = '\n'.join([line for line in text.split('\n') if line != ''])
    text = text.lstrip('\n')
    if text.strip().startswith('def'):
        text = '\n'.join(text.split('\n')[1:])
    # deal with the indentation error
    if text.startswith(' '):
        text = '    ' + text.lstrip()
    else:
        text = '\n'.join(['    ' + line for line in text.split('\n')])
    text = text.split('\n')

    # If number of leading space reduces, we assume that the code block ends.
    min_leading_space = None
    end_index = None
    for index, line in enumerate(text):
        if line.strip() == '' or line.strip()[0] in ["'", '"', '#']:
            continue
        current_leading_space = len(line.rstrip()) - len(line.strip())
        if min_leading_space is None:
            min_leading_space = current_leading_space
        elif current_leading_space < min_leading_space:
            end_index = index
            break
    if end_index is not None:
        text = '\n'.join(text[:end_index])
    else:
        text = '\n'.join(text)
    return text


def humaneval_gpt_postprocess(text: str) -> str:
    """Better answer postprocessor for better instruction-aligned models like
    GPT."""
    if '```' in text:
        blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
        if len(blocks) == 0:
            text = text.split('```')[1]  # fall back to default strategy
        else:
            text = blocks[0]  # fetch the first code block
            if not text.startswith('\n'):  # in case starting with ```python
                text = text[max(text.find('\n') + 1, 0):]
    if text.strip().startswith('from') or text.strip().startswith('import'):
        def_idx = text.find('def')
        if def_idx != -1:
            text = text[max(text.find('\n', def_idx) + 1, 0):]
    text = text.split('\n\n\n')[0]
    if text.strip().startswith('def'):
        text = '\n'.join(text.split('\n')[1:])
    if not text.startswith('    '):
        if text.startswith(' '):
            text = '    ' + text.lstrip()
        else:
            text = '\n'.join(['    ' + line for line in text.split('\n')])
    return text


def extract_python_code(generation: str):
    generation = generation.replace("[PYTHON]", '```python').replace("[/PYTHON]", '```')
    if '```python' in generation:
        p_code = re.compile(r'```python(.*?)```', flags=re.DOTALL)
        try:
            code_block = p_code.findall(generation)[0]
        except:
            code_block = generation
        return code_block
    else:
        codelist = re.split("\ndef|\nclass|\nif|\n#|\nprint", generation)
        return codelist[0]


def extract_python_code_GLM(generation: str):
    generation = generation.replace("[PYTHON]", '```python').replace("[/PYTHON]", '```')
    generation = generation.replace('\\n', '\n')
    generation = generation.replace('\\\"', '"')

    if '```python' in generation:
        p_code = re.compile(r'```python\n(.*?)\n```', flags=re.DOTALL)
        try:
            code_block = p_code.findall(generation)[0]
        except:
            raise RuntimeError
        return code_block
    else:
        codelist = re.split("\ndef|\nclass|\nif|\n#|\nprint", generation)
        return codelist[0]


def gemma2B_postprocess(text):
    if '\n\n\n' in text:
        text = text.split('\n\n\n')[0]
    else:
        text = text.split('```')[0]

    return text
