### 简化版 T-GCN（GCN + GRU）
###构建 GCN 层（图卷积）
import torch
import torch.nn as nn
import torch.nn.functional as F

class GraphConvolution(nn.Module):
    def __init__(self, in_feats, out_feats):
        super(GraphConvolution, self).__init__()
        self.linear = nn.Linear(in_feats, out_feats)

    def forward(self, x, adj):
        # x: [batch, num_nodes, in_feats]
        x = torch.matmul(adj, x)  # 图卷积邻接加权
        x = self.linear(x)
        return F.relu(x)
#### 2. 构建 T-GCN 模型结构（GCN + GRU）
class TGCN(nn.Module):
    def __init__(self, node_num, in_dim, gcn_hidden, gru_hidden, out_dim):
        super(TGCN, self).__init__()
        self.gcn = GraphConvolution(in_dim, gcn_hidden)
        self.gru = nn.GRU(gcn_hidden, gru_hidden, batch_first=True)
        self.out = nn.Linear(gru_hidden, out_dim)

    def forward(self, x_seq, adj):
        # x_seq: [batch, time_steps, nodes, in_dim]
        batch, time, nodes, feat = x_seq.shape
        x_gcn = []
        for t in range(time):
            xt = x_seq[:, t, :, :]  # [batch, nodes, feat]
            xt = self.gcn(xt, adj)  # [batch, nodes, gcn_hidden]
            x_gcn.append(xt)
        x_gcn = torch.stack(x_gcn, dim=1)  # [batch, time, nodes, gcn_hidden]
        x_gcn = x_gcn.view(batch*time, nodes, -1)
        x_gcn = x_gcn.transpose(1, 2)  # GRU expects [batch, time, features]
        x_gcn = x_gcn.view(batch, time, -1)  # [batch, time, nodes * gcn_hidden]
        output, _ = self.gru(x_gcn)  # [batch, time, gru_hidden]
        y = self.out(output[:, -1, :])  # 只取最后一时刻预测
        return y  # [batch, out_dim]

######构造数据 & 示例使用
# 假设有 10 个节点，每个节点 1 维特征，每次序列 12 步
batch_size = 32
time_steps = 12
num_nodes = 10
input_dim = 1

x_seq = torch.randn(batch_size, time_steps, num_nodes, input_dim)

# 构造邻接矩阵（标准化）
adj = torch.eye(num_nodes)
adj = adj / adj.sum(1, keepdim=True)  # 简化的度归一化

# 模型实例
model = TGCN(
    node_num=num_nodes,
    in_dim=input_dim,
    gcn_hidden=16,
    gru_hidden=32,
    out_dim=1  # 每个样本预测一个值（可为 [num_nodes]）
)

# 前向预测
y_pred = model(x_seq, adj)  # 输出: [batch, 1]
