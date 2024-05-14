import os
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


class InferenceEngine:
    def __init__(self, target_dir, base_prompt, api):
        self.target_dir = target_dir
        self.base_prompt = base_prompt
        self.api = api
        from models.openAI_api import OpenAI
        self.api = OpenAI()

    def infer(self, item):

        prompt = self.base_prompt.format(
            language=item['language'], code='{you code here}', question=item['question'])
        solution_path = os.path.join(
            self.target_dir, 'test'+str(item['question_id']), 'solution.py')
        print('---------------------------', self.api)
        print('---------------------------', os.getenv("OPENAI_API_KEY"))
        # 没有才生成
        if not os.path.exists(solution_path):
            result = code_postprocess(self.api.generate(prompt))
            with open(solution_path, 'w') as f:
                f.write(result)
        return solution_path
