from pyspark.sql import SparkSession



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