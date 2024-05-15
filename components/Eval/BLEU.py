from codebleu import calc_codebleu

def codebleu_score(prediction: str, reference: str, language: str = 'python', weights: tuple = (0.1, 0.15, 0.6, 0.15)) -> str:

    result = calc_codebleu([reference], [prediction],
                           lang=language, weights=weights, tokenizer=None)

    result.pop('codebleu')  # 这里dataflow_match_score为0时计算有问题
    result['codebleu'] = weights[0]*result['ngram_match_score']+weights[1]*result['weighted_ngram_match_score'] + \
        weights[2]*result['syntax_match_score'] + \
        weights[3]*result['dataflow_match_score']
    # result is a dictionary with keys:
    # {'codebleu': , 'ngram_match_score': , 'weighted_ngram_match_score':, 'syntax_match_score': , 'dataflow_match_score': }
    return result


