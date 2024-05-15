import re


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


