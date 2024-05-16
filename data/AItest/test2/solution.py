
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

class ImageClassifier(nn.Module):
    def __init__(self, input_size, num_classes):
        super(ImageClassifier, self).__init__()
        self.conv = nn.Conv2d(input_size, 32, kernel_size=3, stride=1, padding=1)
        self.pool = nn.AvgPool2d(kernel_size=2, stride=2)
        self.fc = nn.Linear(32*32*32, num_classes)

    def forward(self, x):
        """
        Input:
        - x: A PyTorch tensor of shape (batch_size, input_size, height, width).

        Output:
        - out: A PyTorch tensor of shape (batch_size, num_classes), representing the output of the image classification model.
        """
        x = self.conv(x)
        x = nn.functional.relu(x)
        x = self.pool(x)
        x = torch.flatten(x, start_dim=1)
        x = self.fc(x)
        return x
