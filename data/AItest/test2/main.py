import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from solution import ImageClassifier
def main():
    # 定义超参数
    input_size = 3  # 输入的维度（对于彩色图像，通常是3）
    num_classes = 10  # 输出的维度（对于CIFAR-10数据集，有10个类别）
    num_epochs = 3  # 训练的轮数
    batch_size = 100  # 每个批次的样本数量
    learning_rate = 0.001  # 学习率

    # 加载CIFAR-10数据集
    transform = transforms.Compose([transforms.ToTensor()])
    train_dataset = torchvision.datasets.CIFAR10(root='./data/AItest/data', train=True, download=True, transform=transform)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # 定义模型
    model = ImageClassifier(input_size, num_classes)

    # 定义损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # 训练模型
    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_loader):
            # 前向传播
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # 反向传播和优化
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            if (i+1) % 100 == 0:
                print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(train_loader)}], Loss: {loss.item()}')
    print("最后的Loss:",loss.item())
    assert loss.item() < 2, "Loss is not less than 2"
    return 1