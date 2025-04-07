###总体结构图（VAE + T-GCN + GNN → 异常检测）
###1️⃣ VAE 编码器（带图感知）
class GraphEncoder(nn.Module):
    def __init__(self, in_feat, latent_dim, node_num):
        super().__init__()
        self.gcn = GraphConvolution(in_feat, 32)
        self.flatten = nn.Flatten()
        self.fc_mu = nn.Linear(32 * node_num, latent_dim)
        self.fc_logvar = nn.Linear(32 * node_num, latent_dim)

    def forward(self, x, adj):
        # x: [batch, nodes, feat]
        h = self.gcn(x, adj)                  # GCN 提取空间特征
        h_flat = self.flatten(h)              # 展平
        mu = self.fc_mu(h_flat)
        logvar = self.fc_logvar(h_flat)
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        z = mu + eps * std                    # reparameterization trick
        return z, mu, logvar

#####  时序建模（T-GCN）
class TemporalGNN(nn.Module):
    def __init__(self, latent_dim, hidden_dim):
        super().__init__()
        self.gru = nn.GRU(latent_dim, hidden_dim, batch_first=True)
        self.out = nn.Linear(hidden_dim, latent_dim)

    def forward(self, z_seq):  # z_seq: [batch, time, latent_dim]
        h, _ = self.gru(z_seq)
        return self.out(h)     # [batch, time, latent_dim]
      
#####3️⃣ 解码器（重构输入）
class Decoder(nn.Module):
    def __init__(self, latent_dim, node_num, feat_dim):
        super().__init__()
        self.fc = nn.Linear(latent_dim, node_num * feat_dim)

    def forward(self, z):
        x_hat = self.fc(z).view(-1, node_num, feat_dim)
        return x_hat

######异常评分（综合）
####重构误差
recon_loss = F.mse_loss(x_hat, x_orig)

#####预测误差（时间序列）：
pred_loss = F.mse_loss(z_pred[:, -1], z_true[:, -1])

#####One-Class SVM on z（非监督检测）：
from sklearn.svm import OneClassSVM
svm = OneClassSVM().fit(z_train[y==0])  # 仅正常训练
y_pred = svm.predict(z_test)


