import os
import json
import csv
import pandas as pd
import json

class SubsetSampler:
    def __init__(self):
        pass

    def write_to_file(self, out_path, data):
        print(f"=> write to file {out_path}")
        if out_path.endswith('.jsonl'):
            with open(out_path, 'w', encoding='utf-8') as f:
                for line in data:
                    json.dump(line, f, ensure_ascii=False)
                    f.write('\n')
        elif out_path.endswith('.csv'):
            with open(out_path, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(data)
        elif out_path.endswith('.json'):
            with open(out_path, 'w') as f:
                json.dump(data, f, ensure_ascii=False)
        else:
            raise Exception("not supported file type")

    def convert_xlsx_to_json_all_sheets(self, path, out_dir):
        # Load the entire workbook
        workbook = pd.ExcelFile(path)

        # Get all sheet names
        sheet_names = workbook.sheet_names

        # Iterate over all sheets
        for sheet_name in sheet_names:
            # Read the specific sheet as a DataFrame
            data = pd.read_excel(path, sheet_name=sheet_name)

            # Get the headers
            headers = data.columns.tolist()

            sample_data = []

            # Iterate over data rows
            for _, row in data.iterrows():
                line = {}

                for header in headers:
                    content = row[header]
                    if isinstance(content, str):
                        content = content.strip()
                    elif pd.isnull(content):
                        content = ""
                    line[header] = content

                sample_data.append(line)

            print(f"Sheet {sheet_name} contains {len(sample_data)} rows.")
            xlsx_out_path = os.path.join(out_dir, f"{sheet_name}.xlsx")
            data.to_excel(f"{xlsx_out_path}", index=False)
            print(f"=> write to file {xlsx_out_path}")

            # Define output path for this sheet
            out_path = os.path.join(out_dir, f"{sheet_name}.json")

            # Write to file
            self.write_to_file(out_path, sample_data)




    def generate_test_cases(self, json_path, output_dir=None):
        # Load the JSON file
        with open(json_path, 'r') as f:
            data = json.load(f)

        # Use the current working directory if no output directory is provided
        if output_dir is None:
            output_dir = os.getcwd()

        # Iterate over all questions
        for item in data:
            question_id = item['question_id']
            language = item['language']
            file_name = item['file_name']
            question = item['question']
            reference = item['reference']
            main = item['main']

            # Create a new directory for each question
            dir_path = os.path.join(output_dir, 'test' + str(question_id))
            os.makedirs(dir_path, exist_ok=True)

            # Write the question to a file
            # with open(os.path.join(dir_path, file_name), 'w') as f:
            #     f.write(question)

            # # Write the reference to a file
            # with open(os.path.join(dir_path, 'reference.txt'), 'w') as f:
            #     f.write(reference)

            # 现在测试用
            with open(os.path.join(dir_path, file_name), 'w') as f:
                f.write(reference)
                
            with open(os.path.join(dir_path, 'reference.txt'), 'w') as f:
                f.write(reference)

            # Write the main content to a file
            with open(os.path.join(dir_path, 'main.py'), 'w') as f:
                f.write(main)

        print("Test cases generated successfully.")


if __name__ == '__main__':
    s = SubsetSampler()
    WORK_DIR = './data/AItest/'
    s.convert_xlsx_to_json_all_sheets(WORK_DIR+'code_scenario.xlsx',WORK_DIR)
    s.generate_test_cases(WORK_DIR+'AI.json',WORK_DIR)
