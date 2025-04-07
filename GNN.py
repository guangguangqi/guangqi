from torch_geometric.data import Data
import torch

# 节点特征（假设有 3 个节点，每个 2 维特征）
x = torch.tensor([[1, 2], [2, 3], [3, 4]], dtype=torch.float)

# 边索引（从 0 到 1，从 1 到 2）
edge_index = torch.tensor([[0, 1],
                           [1, 2]], dtype=torch.long)

# 构建图数据
data = Data(x=x, edge_index=edge_index)

print("节点特征 shape：", data.x.shape)           # [3, 2]
print("边索引 shape：", data.edge_index.shape)   # [2, 2]
