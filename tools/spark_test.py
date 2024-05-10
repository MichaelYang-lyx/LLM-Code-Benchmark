from pyspark.sql import SparkSession
from pyspark import SparkContext


# ------ test 1 ---------
# 初始化一个Spark会话
spark = SparkSession.builder \
    .appName("Word Count Example") \
    .getOrCreate()

# 从文本文件创建一个RDD
text_file = spark.sparkContext.textFile("tools/example.txt")

# 执行一个词频统计
word_counts = text_file.flatMap(lambda line: line.split(" ")) \
                       .map(lambda word: (word, 1)) \
                       .reduceByKey(lambda a, b: a + b)

# 打印结果
for word, count in word_counts.collect():
    print(f"{word}: {count}")

# ------- test 2 ------- 
# 创建一个简单的RDD
sc = SparkContext("local", "Example")
rdd = sc.parallelize(["apple", "banana", "cherry"])

# 定义map函数
def get_length(s):
    return (s, len(s))  # 返回一个键值对

# 应用map函数
mapped_rdd = rdd.map(get_length)

# 行动操作，输出结果
print(mapped_rdd.collect())