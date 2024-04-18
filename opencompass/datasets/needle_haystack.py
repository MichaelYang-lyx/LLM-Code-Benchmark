import json
import os

import tiktoken

from datasets import Dataset, DatasetDict

from opencompass.openicl import BaseEvaluator
from opencompass.registry import LOAD_DATASET, TEXT_POSTPROCESSORS

from transformers import AutoTokenizer


from .base import BaseDataset
import re
import numpy as np

import chardet


class NH_Helper():
    def __init__(self, tokenizer_name) -> None:
        self.tokenizer_name = tokenizer_name

        if tokenizer_name == 'sensetime':
            tokenizer_model = 'tools/test_tokenizer/sensechat_v4.1.0_tokenizer'
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_model)
        elif tokenizer_name.startswith('gpt'):
            self.tokenizer = tiktoken.encoding_for_model(tokenizer_name)
        elif tokenizer_name == 'text':
            pass

    def read_context_files(self, path):
        context = ""

        with open(path, 'rb') as file:
            raw_data = file.read()
            encoding = chardet.detect(raw_data)['encoding']

        with open(path, 'r', encoding=encoding, errors='replace') as f:
            context += f.read()

        context = context.replace('\n', '')

        return context

    def generate(self, needle, context, depth_percent, context_length):
        # trim context to context length
        context = self.encode_and_trim(context, context_length)
        # insert needle to certain postion
        context = self.insert_needle(needle, context, depth_percent, context_length)

        return context


    def encode_context(self, context):
        if self.tokenizer_name != 'text':
            return self.tokenizer.encode(context)
        else:
            return context

    def decode_tokens(self, tokens):
        if self.tokenizer_name != 'text':
            return self.tokenizer.decode(tokens)
        else:
            return tokens

    def encode_and_trim(self, context, context_length):
        tokens = self.encode_context(context)
        # print(f'text len: {len(context)}  tokens len: {len(tokens)}')
        if len(tokens) > context_length:
            context = self.decode_tokens(tokens[:context_length])

        return context

    def insert_needle(self, needle, context, depth_percent, context_length):
        tokens_needle = self.encode_context(needle)
        tokens_context = self.encode_context(context)

        # Reducing the context length by 150 buffer. This is to account for system message, the user question, and response.
        context_length -= 150

        # If your context + needle are longer than the context length (which it will be), then reduce tokens from the context by the needle length
        if len(tokens_context) + len(tokens_needle) > context_length:
            tokens_context = tokens_context[:context_length - len(tokens_needle)]

        if depth_percent == 100:
            # If your depth percent is 100 (which means your needle is the last thing in the doc), throw it at the end
            tokens_new_context = tokens_context + tokens_needle
        else:
            # Go get the position (in terms of tokens) to insert your needle
            insertion_point = int(len(tokens_context) * (depth_percent / 100))

            # tokens_new_context represents the tokens before the needle
            tokens_new_context = tokens_context[:insertion_point]

            # We want to make sure that we place our needle at a sentence break so we first see what token a '.' is
            period_tokens = self.encode_context('。')
            
            # Then we iteration backwards until we find the first period
            while tokens_new_context and tokens_new_context[-1] not in period_tokens:
                insertion_point -= 1
                tokens_new_context = tokens_context[:insertion_point]

            # Once we get there, then add in your needle, and stick the rest of your context in on the other end.
            # Now we have a needle in a haystack
            tokens_new_context += tokens_needle + tokens_context[insertion_point:]

        # print('new tokens: ', len(tokens_new_context))
        # Convert back to a string and return it
        new_context = self.decode_tokens(tokens_new_context)

        return new_context



@LOAD_DATASET.register_module()
class NeedleInHaystack(BaseDataset):
    '''
    ref: https://github.com/gkamradt/LLMTest_NeedleInAHaystack
    '''

    @staticmethod
    def load(path, needle, must_have, tokenizer_name, repeat_times = 3, context_lengths_min = 1000, context_lengths_max = 200000, context_lengths_num_intervals = 35, document_depth_num_intervals=20):

        context_lengths = np.round(np.linspace(context_lengths_min, context_lengths_max, num=context_lengths_num_intervals, endpoint=True)).astype(int)
        
        document_depth_percents = np.round(np.linspace(0, 100, num=document_depth_num_intervals, endpoint=True)).astype(int)

        helper = NH_Helper(tokenizer_name)
        context = helper.read_context_files(path)

        dataset = []

        for context_length in context_lengths:
            for depth_percent in document_depth_percents:
                # print(f'process context_length {context_length} depth_percent {depth_percent}')

                new_context = helper.generate(needle, context, depth_percent, context_length)

            
                for _ in range(repeat_times):
                    dataset.append({
                        'context':  new_context,
                        'needle': f"{context_length}-{depth_percent}-{needle}-{must_have}"
                    })
        dataset = Dataset.from_list(dataset)

        return dataset


class NeedleInHaystackEvaluator(BaseEvaluator):
    def score(self, predictions, references) -> dict:
        if len(predictions) != len(references):
            return {
                'error': 'predictions and references have different lengths'
            }
        

        total_score = 0
        details = []

        for prediction, reference in zip(predictions, references):
            prediction = re.sub(r'\s+', '', prediction)
            reference = re.sub(r'\s+', '', reference)

            context_length = int(reference.split('-')[0])
            doc_depth = int(reference.split('-')[1])
            must_have = reference.split('-')[3]

            if must_have in prediction:
                score = 100.0
            else:
                score = 0

            details.append({
                'context-length': context_length,
                'doc-depth': doc_depth,
                'score': score,
            })

            total_score += score

        average_score = total_score / len(predictions) if predictions else 0
        result = {'score': average_score, 'details': details}
        return result

    

@TEXT_POSTPROCESSORS.register_module('needle')
def needle_haystack_postprocess(text):
    return text

