# 使用PyTorch镜像作为基础镜像
FROM pytorch/pytorch

# Install OpenJDK-8
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean;
    
# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

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
RUN pip install pandas
RUN pip install openpyxl
RUN pip install pyspark
RUN pip install python-dotenv
RUN pip install langchain
RUN pip install langchain_openai

