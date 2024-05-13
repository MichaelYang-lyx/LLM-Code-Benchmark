import torch
import torch.nn as nn
import numpy as np
from solution import LinearRegression


def main():
    # 定义模型
    input_dim = 1  # 输入的维度
    output_dim = 1  # 输出的维度

    model = LinearRegression(input_dim, output_dim)

    # 定义损失函数和优化器
    criterion = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

    # 训练模型
    epochs = 100
    # 数据集
    np.random.seed(0)
    x = np.random.rand(10, 1)
    y = 2 * x + 3 + np.random.randn(10, 1)

    # 将numpy数组转换为PyTorch Tensor
    x = torch.from_numpy(x).float()
    y = torch.from_numpy(y).float()

    for epoch in range(epochs):
        # 前向传播
        outputs = model(x)
        loss = criterion(outputs, y)

        # 反向传播和优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (epoch+1) % 10 == 0:
            print(f'Epoch {epoch+1}/{epochs}, Loss: {loss.item()}')
    print("Final Loss:", loss.item())
    # 在训练循环结束后
    assert loss.item() < 2, "Loss is not less than 2"
    return 1.0
