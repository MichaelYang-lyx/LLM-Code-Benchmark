import os
import sys
import importlib.util
from tqdm import tqdm



TARGET_DIR='./data/AItest'
# 获取当前目录下所有的子文件夹
folders = [f.name for f in os.scandir(TARGET_DIR) if f.is_dir()]

# 过滤出以'test'开头的子文件夹
test_folders = [folder for folder in folders if folder.startswith('test')]

def get_score(folder):
    main_file = os.path.join(TARGET_DIR, folder, 'main.py')
    if os.path.isfile(main_file):
        # 添加main.py所在的目录到sys.path
        sys.path.insert(0, os.path.join(TARGET_DIR, folder))
        spec = importlib.util.spec_from_file_location("main", main_file)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            score = module.main()  # 假设 main 函数返回分数
            print(f"分数: {score}")
        except Exception as e:
            print(f"运行 {main_file} 出错: {str(e)}")
            # 在这里采用另一种方式计算分数
            score = 0  # 假设这是你的备用计分函数
            print(f"使用备用方法计算的分数: {score}")
        # 从sys.path中移除main.py所在的目录
        sys.path.pop(0)
    else:
        print(f"在{folder}文件夹中没有找到main.py文件")
    return score




for folder in tqdm(test_folders, desc="Running tests", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
    print("---------- ", os.path.join(TARGET_DIR, folder, 'main.py'), " 运行 ----------")
    score = get_score(folder)
