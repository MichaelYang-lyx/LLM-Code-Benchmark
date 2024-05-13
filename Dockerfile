# 使用PyTorch镜像作为基础镜像
FROM pytorch/pytorch

# 更新apt-get并安装gcc和g++
RUN apt-get update && apt-get install -y gcc g++

# 安装你需要的包
RUN pip install codebleu
RUN pip install openai
RUN pip install dashscope
RUN pip install tiktoken
RUN pip install zhipuai
RUN pip install mmengine
RUN pip install jieba
RUN pip install pyspark
RUN pip install python-dotenv

# sudo add-apt-repository ppa:webupd8team/java
# sudo apt-get update
# sudo apt-get install oracle-java8-installer