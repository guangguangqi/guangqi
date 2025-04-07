import torch
import torch.nn as nn
# 构建 VAE 模型（用 PyTorch 举例）
# 假设输入图像为 28x28（如 MNIST）
class VAE(nn.Module):
    def __init__(self, latent_dim=16):
        super(VAE, self).__init__()
        self.encoder = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28*28, 256),
            nn.ReLU()
        )
        self.fc_mu = nn.Linear(256, latent_dim)
        self.fc_logvar = nn.Linear(256, latent_dim)
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 28*28),
            nn.Sigmoid()  # 输出归一化到 [0, 1]
        )

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std  # 采样 z

    def forward(self, x):
        x_encoded = self.encoder(x)
        mu = self.fc_mu(x_encoded)
        logvar = self.fc_logvar(x_encoded)
        z = self.reparameterize(mu, logvar)
        x_recon = self.decoder(z).view(-1, 1, 28, 28)
        return x_recon, mu, logvar
#   定义损失函数（重构 + KL 散度）     
    def vae_loss(x, x_recon, mu, logvar):
    recon_loss = F.mse_loss(x_recon, x, reduction='mean')
    kl_div = -0.5 * torch.mean(1 + logvar - mu.pow(2) - logvar.exp())
    return recon_loss + kl_div

# 训练模型
from torch.utils.data import DataLoader, TensorDataset

# 转为 Tensor
X_tensor = torch.tensor(X, dtype=torch.float32)
loader = DataLoader(TensorDataset(X_tensor), batch_size=64, shuffle=True)

vae = VAE(input_dim=X.shape[1], latent_dim=2)  # 压缩到 2 维空间
optimizer = torch.optim.Adam(vae.parameters(), lr=1e-3)

for epoch in range(100):
    for batch in loader:
        x = batch[0]
        x_recon, mu, logvar = vae(x)
        loss = vae_loss(x, x_recon, mu, logvar)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

# 获取低维潜在表示
vae.eval()
with torch.no_grad():
    _, mu, _ = vae(X_tensor)
    z = mu.numpy()  # shape: [N, latent_dim]
#可视化潜在空间
import matplotlib.pyplot as plt

plt.scatter(z[:, 0], z[:, 1], c='blue', s=5)
plt.xlabel('z1')
plt.ylabel('z2')
plt.title('Plasma States in Latent Space')
plt.grid(True)
plt.show()
