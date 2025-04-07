import torch
import torch.nn as nn
import torch.nn.functional as F

# 输入图像张量：[批量数, 通道数, 高度, 宽度]
x = torch.randn(4, 3, 64, 64)  # 4张64x64的RGB图像

# 一个简单的CNN模型
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc = nn.Linear(16 * 32 * 32, num_classes)  # 假设输入为64x64

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # shape: [4, 16, 32, 32]
        x = x.view(x.size(0), -1)             # 展平：[4, 16*32*32]
        x = self.fc(x)                        # 输出 logits：[4, 10]
        return x

model = SimpleCNN(num_classes=10)
output = model(x)

print("输出 logits 形状：", output.shape)  # torch.Size([4, 10])
