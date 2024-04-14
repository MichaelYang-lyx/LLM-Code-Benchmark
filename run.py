# 使用示例
model = ...  # 这里是你的模型
data = ...  # 这里是你的数据
labels = ...  # 这里是你的标签

infer = Infer(model)
predictions = infer.predict(data)

eval = Eval(predictions, labels)
evaluation_results = eval.evaluate()

summarizer = Summarizer(evaluation_results)
summary = summarizer.summarize()

print(summary)