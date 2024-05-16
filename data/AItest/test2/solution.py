
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

class ImageClassifier(nn.Module):
    def __init__(self, input_size, num_classes):
        super(ImageClassifier, self).__init__()
        self.conv = nn.Conv2d(input_size, 32, kernel_size=3, stride=1, padding=1)
        self.fc = nn.Linear(32*32*32, num_classes)

    def forward(self, x):
        x = self.conv(x)
        x = nn.ReLU()(x)
        x = nn.AvgPool2d(kernel_size=2)(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x
