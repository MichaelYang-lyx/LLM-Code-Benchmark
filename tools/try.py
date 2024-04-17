# 首先，你需要安装python-dotenv库，可以使用pip进行安装：
# pip install python-dotenv

# 导入所需的库
from dotenv import load_dotenv
import os

# 加载.env文件
load_dotenv()

# 获取.env文件中的变量
var = os.getenv('OPENAI_API_KEY')

# 打印变量
print(var)
