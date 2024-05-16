import torch
import torch.nn as nn
import numpy as np
from solution import LinearRegression

def main():
    # ����ģ��
    input_dim = 1  # �����ά��
    output_dim = 1  # �����ά��

    model = LinearRegression(input_dim, output_dim)

    # ������ʧ�������Ż���
    criterion = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

    # ѵ��ģ��
    epochs = 100
    # ���ݼ�
    np.random.seed(0)
    x = np.random.rand(10, 1)
    y = 2 * x + 3 + np.random.randn(10, 1)

    # ��numpy����ת��ΪPyTorch Tensor
    x = torch.from_numpy(x).float()
    y = torch.from_numpy(y).float()

    for epoch in range(epochs):
        # ǰ�򴫲�
        outputs = model(x)
        loss = criterion(outputs, y)
        
        # ���򴫲����Ż�
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (epoch+1) % 10 == 0:
            print(f'Epoch {epoch+1}/{epochs}, Loss: {loss.item()}')
    print("Final Loss:",loss.item())
    # ��ѵ��ѭ��������
    assert loss.item() < 2, "Loss is not less than 2"
    return 1