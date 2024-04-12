import os
import subprocess


import os


TARGET_DIR='./data/AItest'
# 获取当前目录下所有的子文件夹

folders = [f.name for f in os.scandir(TARGET_DIR) if f.is_dir()]

# 过滤出以'test'开头的子文件夹
test_folders = [folder for folder in folders if folder.startswith('test')]
print(test_folders)
# 遍历这些文件夹，并运行每个文件夹下的main.py文件
for folder in test_folders:
    main_file = os.path.join(TARGET_DIR, folder, 'main.py')
    print("---------- ",main_file," 运行 ----------")
    if os.path.isfile(main_file):
        subprocess.run(['python', main_file])
    else:
        print(f"在{folder}文件夹中没有找到main.py文件")
