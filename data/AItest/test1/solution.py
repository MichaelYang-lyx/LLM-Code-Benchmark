import torch.nn as nn

class LinearRegression(nn.Module):
    def __init__(self, input_size, output_size):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(input_size, output_size)

    def forward(self, x):
        """
        输入:
        - x: 一个形状为(batch_size, input_size)的PyTorch张量。1111

        输出:
        - out: 一个形状为(batch_size, output_size)的PyTorch张量，表示线性回归模型的输出。
        """
        out = self.linear(x)
        return out