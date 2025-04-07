# PyTorch 简化示例（图像任务）：
import torch
import torch.nn as nn

z = torch.randn(64, 100)  # 输入噪声，形状 [batch_size, latent_dim]

# 假设生成 28x28 灰度图像（如 MNIST）
class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(100, 256),
            nn.ReLU(),
            nn.Linear(256, 28*28),
            nn.Tanh()  # 输出范围 [-1, 1]
        )

    def forward(self, z):
        x_fake = self.net(z).view(-1, 1, 28, 28)
        return x_fake

G = Generator()
x_fake = G(z)  # 输出假图像，shape: [64, 1, 28, 28]

# 判别器输入与输出
class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28*28, 128),
            nn.LeakyReLU(0.2),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x)

D = Discriminator()
prob = D(x_fake)  # 输出假图像的“真假概率”，shape: [64, 1]
