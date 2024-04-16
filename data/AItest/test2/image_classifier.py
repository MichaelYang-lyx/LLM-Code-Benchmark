import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

class ImageClassifier(nn.Module):
    def __init__(self, input_size, num_classes):
        super(ImageClassifier, self).__init__()
        self.conv = nn.Conv2d(input_size, 32, kernel_size=3, stride=1, padding=1)
        self.fc = nn.Linear(32*16*16, num_classes)

    def forward(self, x):
        """
        输入:
        - x: 一个形状为(batch_size, input_size, height, width)的PyTorch张量。

        输出:
        - out: 一个形状为(batch_size, num_classes)的PyTorch张量，表示图像分类模型的输出。
        """
         # 卷积操作
        x = self.conv(x)
        # ReLU激活函数
        x = torch.relu(x)
        # 平均池化操作
        x = nn.functional.avg_pool2d(x, 2)
        # 展平操作
        x = x.view(x.size(0), -1)
        # 线性变换
        out = self.fc(x)
        return out
