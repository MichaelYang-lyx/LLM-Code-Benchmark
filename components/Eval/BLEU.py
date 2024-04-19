from codebleu import calc_codebleu
import re

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


def code_postprocess(text: str, language: str = 'python') -> str:

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
        # blocks = re.findall(r'```{language}```', text, re.DOTALL)
        blocks = re.findall(fr'```{language}(.*?)```', text, re.DOTALL)

        if len(blocks) == 0:
            text = text.split('```')[1]  # fall back to default strategy
        else:
            text = blocks[0]  # fetch the first code block
            if not text.startswith('\n'):  # in case starting with ```python
                text = text[max(text.find('\n') + 1, 0):]

    return text