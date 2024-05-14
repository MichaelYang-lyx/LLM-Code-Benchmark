import os
import sys
import importlib.util
import contextlib
from .BLEU import codebleu_score


class ScoreCalculator:
    def __init__(self, target_dir, output_dir):
        self.target_dir = target_dir
        self.output_dir = output_dir

    def get_score(self, data_folder):
        main_file = os.path.join(self.target_dir, data_folder, 'main.py')
        solution_file = os.path.join(
            self.target_dir, data_folder, 'solution.py')
        reference_file = os.path.join(
            self.target_dir, data_folder, 'reference.txt')

        if os.path.isfile(main_file):
            # Add the directory of main.py to sys.path
            if "main" in sys.modules:
                del sys.modules["main"]
            if "solution" in sys.modules:
                del sys.modules["solution"]
            sys.path.insert(0, os.path.join(self.target_dir, data_folder))
            spec = importlib.util.spec_from_file_location("main", main_file)
            module = importlib.util.module_from_spec(spec)

        log = os.path.join(self.output_dir, 'log.txt')

        if not os.path.exists(data_folder):

            try:
                with open(log, 'a') as f, contextlib.redirect_stdout(f):
                    print("---------- Running ", main_file, " ----------")
                    spec.loader.exec_module(module)
                    score = module.main()  # Assume main function returns score

            except Exception as e:
                print(f"Running {main_file} error: {str(e)}")

                # Use another way to calculate score here
                if os.path.isfile(solution_file):
                    with open(solution_file, 'r') as f:
                        solution_content = f.read()
                else:
                    print(
                        f"Did not find solution.py file in {data_folder} folder")

                if os.path.isfile(reference_file):
                    with open(reference_file, 'r') as f:
                        reference_content = f.read()
                else:
                    print(
                        f"Did not find reference.txt file in {data_folder} folder")

                score = codebleu_score(solution_content, reference_content)[
                    'codebleu']
            # Remove the directory of main.py from sys.path
            sys.path.remove(os.path.join(self.target_dir, data_folder))

        else:
            print(f"Did not find main.py file in {data_folder} folder")

        # get solution and reference content

        return score
