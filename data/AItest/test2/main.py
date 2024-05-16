import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from solution import ImageClassifier
def main():
    # ���峬����
    input_size = 3  # �����ά�ȣ����ڲ�ɫͼ��ͨ����3��
    num_classes = 10  # �����ά�ȣ�����CIFAR-10���ݼ�����10�����
    num_epochs = 3  # ѵ��������
    batch_size = 100  # ÿ�����ε���������
    learning_rate = 0.001  # ѧϰ��

    # ����CIFAR-10���ݼ�
    transform = transforms.Compose([transforms.ToTensor()])
    train_dataset = torchvision.datasets.CIFAR10(root='./data/AItest/data', train=True, download=True, transform=transform)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # ����ģ��
    model = ImageClassifier(input_size, num_classes)

    # ������ʧ�������Ż���
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # ѵ��ģ��
    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_loader):
            # ǰ�򴫲�
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # ���򴫲����Ż�
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            if (i+1) % 100 == 0:
                print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(train_loader)}], Loss: {loss.item()}')
    print("����Loss:",loss.item())
    assert loss.item() < 2, "Loss is not less than 2"
    return 1