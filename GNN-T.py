# ============================================================
# Graph Transformer for Antibody Pretraining (OAS + SAbDab)
# Code in English, with concise Chinese notes.
# Requirements:
#   pip install torch torch_geometric pandas numpy
# (and appropriate pyg wheels for your CUDA; see PyG docs)
# ============================================================

import os
import math
import numpy as np
import pandas as pd
from typing import Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset

from torch_geometric.data import Data, DataLoader
from torch_geometric.nn import TransformerConv, global_mean_pool

# ---------------------------
# Utility: edge builders
# ---------------------------

def build_sequential_edges(L: int) -> torch.Tensor:
    """Build backbone (i,i+1) edges for a chain of length L.
    中文：构建主链顺序边 (i, i+1)
    """
    src = torch.arange(0, L - 1, dtype=torch.long)
    dst = src + 1
    edges = torch.stack([torch.cat([src, dst]), torch.cat([dst, src])], dim=0)
    return edges  # [2, 2*(L-1)] (undirected)

def pairwise_dist(coords: torch.Tensor) -> torch.Tensor:
    """Compute pairwise distances between coordinates.
    coords: [L, 3]
    中文：计算坐标两两欧氏距离
    """
    diff = coords[:, None, :] - coords[None, :, :]
    return torch.sqrt(torch.sum(diff * diff, dim=-1) + 1e-9)  # [L, L]

def build_spatial_edges_from_coords(coords: torch.Tensor,
                                    dist_threshold: float = 8.0,
                                    topk: Optional[int] = None) -> torch.Tensor:
    """Build spatial edges using CA coordinate proximity.
    - dist_threshold: connect pairs with distance <= threshold
    - topk: alternatively, connect top-k nearest neighbors per residue
    中文：基于CA空间邻近建立边（阈值或k近邻）
    """
    L = coords.size(0)
    D = pairwise_dist(coords)  # [L, L]
    mask = torch.ones_like(D, dtype=torch.bool)
    mask.fill_(True)
    mask = mask.fill_(True)
    # Remove self connections
    D[torch.arange(L), torch.arange(L)] = float('inf')

    if topk is not None:
        # For each i, select top-k nearest j
        nn_idx = torch.topk(-D, k=min(topk, L-1), dim=-1).indices  # negative for smallest
        src = torch.arange(L).unsqueeze(1).expand(-1, nn_idx.size(1)).reshape(-1)
        dst = nn_idx.reshape(-1)
    else:
        sel = (D <= dist_threshold).nonzero(as_tuple=False)
        src, dst = sel[:, 0], sel[:, 1]

    # Make undirected
    edge_index = torch.stack([torch.cat([src, dst]), torch.cat([dst, src])], dim=0)
    return edge_index

def rbf_expand(dist: torch.Tensor, K: int = 16, dmin: float = 0.0, dmax: float = 20.0) -> torch.Tensor:
    """RBF expansion for distances.
    中文：将距离用高斯基展开，便于模型使用连续几何信息
    """
    centers = torch.linspace(dmin, dmax, K, device=dist.device)
    gamma = (dmax - dmin) / K
    dist = dist.unsqueeze(-1)  # [E, 1]
    return torch.exp(-((dist - centers) ** 2) / (gamma ** 2))  # [E, K]

# ---------------------------
# Dataset
# ---------------------------

class AntibodyGraphDataset(Dataset):
    """
    Unified dataset that can read:
      - OAS sequence embeddings (per-residue .npy): seq_emb_path
      - SAbDab coordinates (per-residue Cα .npy): coords_path
      - Optional node labels (e.g., paratope 0/1) or graph labels

    Manifest CSV columns (example):
        id,source,seq_emb_path,coords_path,aa_idx_path,label_path
      where:
        - source in {"OAS","SAbDab"}
        - seq_emb_path: path to numpy array [L, D_seq]
        - coords_path:  path to numpy array [L, 3] (empty for OAS rows)
        - aa_idx_path:  optional numpy array [L] of residue indices (0..20), can be -1 if masked
        - label_path:   optional numpy array [L] for node labels or [1] for graph label

    中文：
      - 本数据集统一从清单CSV加载OAS序列嵌入和SAbDab结构坐标
      - 若无结构则仅建顺序边；若有结构则建空间边（并可叠加顺序边）
    """

    def __init__(self,
                 manifest_csv: str,
                 add_sequential_edges: bool = True,
                 spatial_topk: Optional[int] = 16,
                 spatial_threshold: Optional[float] = None,
                 use_rbf_edge_attr: bool = True,
                 rbf_K: int = 16):
        super().__init__()
        self.df = pd.read_csv(manifest_csv)
        self.add_sequential_edges = add_sequential_edges
        self.spatial_topk = spatial_topk
        self.spatial_threshold = spatial_threshold
        self.use_rbf_edge_attr = use_rbf_edge_attr
        self.rbf_K = rbf_K

    def __len__(self) -> int:
        return len(self.df)

    def _safe_load_npy(self, path: str) -> Optional[np.ndarray]:
        if isinstance(path, str) and len(path) > 0 and os.path.exists(path):
            return np.load(path, allow_pickle=False)
        return None

    def __getitem__(self, idx: int) -> Data:
        row = self.df.iloc[idx]
        # Load sequence embeddings (required)
        seq_arr = self._safe_load_npy(row['seq_emb_path'])
        if seq_arr is None:
            raise FileNotFoundError(f"Missing seq_emb_path for row {idx}: {row['seq_emb_path']}")
        seq_emb = torch.tensor(seq_arr, dtype=torch.float)  # [L, D_seq]
        L, D_seq = seq_emb.shape

        # Optional amino-acid indices (for MLM or supervised node labels)
        aa_idx_arr = self._safe_load_npy(row.get('aa_idx_path', '')) if 'aa_idx_path' in self.df.columns else None
        aa_idx = torch.tensor(aa_idx_arr, dtype=torch.long) if aa_idx_arr is not None else None  # [L]

        # Optional labels (node-level or graph-level)
        label_arr = self._safe_load_npy(row.get('label_path', '')) if 'label_path' in self.df.columns else None
        if label_arr is not None and label_arr.ndim == 1 and label_arr.shape[0] == L:
            y = torch.tensor(label_arr, dtype=torch.long)  # node-level labels
        elif label_arr is not None:
            y = torch.tensor(label_arr, dtype=torch.float)  # graph-level or scalar
        else:
            y = None

        # Coordinates (for SAbDab entries)
        coords_arr = self._safe_load_npy(row.get('coords_path', '')) if 'coords_path' in self.df.columns else None
        coords = torch.tensor(coords_arr, dtype=torch.float) if coords_arr is not None else None  # [L, 3]

        # Build edges
        edge_index_list = []
        edge_type_list = []  # 0=seq, 1=spatial
        edge_attr_list = []

        # Sequential edges (backbone)
        if self.add_sequential_edges:
            e_seq = build_sequential_edges(L)  # [2, E_seq]
            edge_index_list.append(e_seq)
            edge_type_list.append(torch.zeros(e_seq.size(1), dtype=torch.long))  # type 0
            if self.use_rbf_edge_attr:
                # For sequential edges, we can encode a fixed "pseudo-distance" (e.g., 3.8Å) or 1-step hop
                dist_seq = torch.full((e_seq.size(1),), 3.8, dtype=torch.float)
                edge_attr_list.append(rbf_expand(dist_seq, K=self.rbf_K))

        # Spatial edges (from coords if present)
        if coords is not None:
            if self.spatial_topk is not None:
                e_sp = build_spatial_edges_from_coords(coords, topk=self.spatial_topk)
            else:
                thr = self.spatial_threshold if self.spatial_threshold is not None else 8.0
                e_sp = build_spatial_edges_from_coords(coords, dist_threshold=thr)

            edge_index_list.append(e_sp)
            edge_type_list.append(torch.ones(e_sp.size(1), dtype=torch.long))  # type 1

            if self.use_rbf_edge_attr:
                # Compute distances for these edges
                src, dst = e_sp[0], e_sp[1]
                d = torch.linalg.norm(coords[src] - coords[dst], dim=-1)  # [E_sp]
                edge_attr_list.append(rbf_expand(d, K=self.rbf_K))

        # Concatenate edges
        if len(edge_index_list) == 0:
            # Fallback: at least sequential edges
            e_seq = build_sequential_edges(L)
            edge_index = e_seq
            edge_type = torch.zeros(e_seq.size(1), dtype=torch.long)
            edge_attr = rbf_expand(torch.full((e_seq.size(1),), 3.8, dtype=torch.float), K=self.rbf_K) \
                        if self.use_rbf_edge_attr else None
        else:
            edge_index = torch.cat(edge_index_list, dim=1)
            edge_type = torch.cat(edge_type_list, dim=0)
            edge_attr = torch.cat(edge_attr_list, dim=0) if self.use_rbf_edge_attr and len(edge_attr_list) > 0 else None

        # Package Data
        data = Data(
            x=seq_emb,                 # node features: sequence LM embedding [L, D_seq]
            edge_index=edge_index,     # [2, E]
            y=y                        # optional labels
        )
        # Store extra fields
        data.edge_type = edge_type    # 中文：边类型(顺序/空间)
        if edge_attr is not None:
            data.edge_attr = edge_attr  # RBF-expanded distances etc.
        if coords is not None:
            data.coords = coords       # coordinates if available
        if aa_idx is not None:
            data.aa_idx = aa_idx       # amino-acid indices (0..20)

        # chain type, source, id (optional metadata)
        data.source = row.get('source', 'UNKNOWN')
        data.sample_id = row.get('id', f'sample_{idx}')
        return data

# ---------------------------
# Model: Node/Edge encoders + Graph Transformer
# ---------------------------

class EdgeTypeEmbedding(nn.Module):
    """Embed edge type (seq/spatial) and concatenate with geometric RBF.
    中文：边类型嵌入（顺序/空间），与RBF几何特征拼接
    """
    def __init__(self, etype_vocab: int = 2, etype_dim: int = 8, rbf_K: int = 16, out_dim: int = 64):
        super().__init__()
        self.etype_emb = nn.Embedding(etype_vocab, etype_dim)
        self.lin = nn.Linear(etype_dim + rbf_K, out_dim)

    def forward(self, edge_type: torch.Tensor, edge_attr_rbf: torch.Tensor) -> torch.Tensor:
        et = self.etype_emb(edge_type)                  # [E, etype_dim]
        x = torch.cat([et, edge_attr_rbf], dim=-1)      # [E, etype_dim + rbf_K]
        return self.lin(x)                               # [E, out_dim]

class NodeEncoder(nn.Module):
    """Project sequence LM embeddings to model hidden size.
    中文：将序列语言模型嵌入投影到隐藏维度
    """
    def __init__(self, seq_dim: int, hidden: int):
        super().__init__()
        self.proj = nn.Linear(seq_dim, hidden)
        self.norm = nn.LayerNorm(hidden)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.norm(F.gelu(self.proj(x)))

class GraphTransformer(nn.Module):
    """Stack of TransformerConv with edge attributes.
    中文：带边特征的Transformer卷积堆叠
    """
    def __init__(self, hidden: int, edge_dim: int, heads: int = 8, layers: int = 6, dropout: float = 0.1):
        super().__init__()
        self.layers = nn.ModuleList([
            TransformerConv(
                in_channels=hidden,
                out_channels=hidden // heads,
                heads=heads,
                edge_dim=edge_dim,
                beta=True,
                dropout=dropout
            )
            for _ in range(layers)
        ])
        self.norms = nn.ModuleList([nn.LayerNorm(hidden) for _ in range(layers)])
        self.act = nn.GELU()

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor, edge_feat: Optional[torch.Tensor]) -> torch.Tensor:
        for conv, norm in zip(self.layers, self.norms):
            h = conv(x, edge_index, edge_feat)
            x = norm(x + h)           # residual
            x = self.act(x)
        return x

class AntibodyGraphModel(nn.Module):
    """
    End-to-end model:
      - NodeEncoder for sequence LM embeddings
      - EdgeTypeEmbedding (+ RBF) for edges
      - GraphTransformer backbone
      - Heads for node- or graph-level tasks

    中文：端到端模型（节点特征来自序列LM，边特征来自类型+RBF，主体为图Transformer）
    """
    def __init__(self,
                 seq_dim: int,
                 hidden: int = 512,
                 edge_out_dim: int = 64,
                 heads: int = 8,
                 layers: int = 6,
                 dropout: float = 0.1,
                 num_node_classes: int = 2):
        super().__init__()
        self.node_enc = NodeEncoder(seq_dim, hidden)
        self.edge_enc = EdgeTypeEmbedding(etype_vocab=2, etype_dim=8, rbf_K=16, out_dim=edge_out_dim)
        self.backbone = GraphTransformer(hidden, edge_out_dim, heads, layers, dropout)
        # Node-level head (e.g., paratope classification). Change to graph-level if needed.
        self.node_head = nn.Sequential(
            nn.Linear(hidden, hidden),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.LayerNorm(hidden),
            nn.Linear(hidden, num_node_classes)
        )

    def forward(self, data: Data) -> torch.Tensor:
        x = self.node_enc(data.x)  # [N, hidden]
        if hasattr(data, 'edge_attr'):
            edge_feat = self.edge_enc(data.edge_type.to(x.device), data.edge_attr.to(x.device))
        else:
            # 如果没有RBF边特征，只用边类型嵌入 + 零RBF
            zeros_rbf = torch.zeros(data.edge_index.size(1), 16, device=x.device)
            edge_feat = self.edge_enc(data.edge_type.to(x.device), zeros_rbf)
        h = self.backbone(x, data.edge_index, edge_feat)
        logits = self.node_head(h)  # node-level logits [N, C]
        return logits

# ---------------------------
# Training / Evaluation
# ---------------------------

def collate_to_device(batch, device):
    from torch_geometric.loader.dataloader import Collater
    collate = Collater([], [])
    data = collate(batch)
    return data.to(device)

def train_epoch(model, loader, optimizer, device):
    model.train()
    total_loss = 0.0
    total_nodes = 0
    for batch in loader:
        data = batch.to(device)
        optimizer.zero_grad()
        logits = model(data)          # [N, C] for node classification
        if data.y is None:
            # 没有监督标签时可替换为自监督损失（如MLM/对比学习）
            continue
        if data.y.dim() == 1 and logits.size(0) == data.y.size(0):
            loss = F.cross_entropy(logits, data.y)  # node-level CE
            nodes = data.y.numel()
        else:
            # Extend here for graph-level tasks (pooling + regression/classification)
            raise ValueError("Unexpected label shape; provide node-level y of shape [N] or adapt head.")
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
        optimizer.step()
        total_loss += loss.item() * nodes
        total_nodes += nodes
    return total_loss / max(1, total_nodes)

@torch.no_grad()
def evaluate(model, loader, device):
    model.eval()
    total_correct = 0
    total_nodes = 0
    for batch in loader:
        data = batch.to(device)
        logits = model(data)
        if data.y is None:
            continue
        pred = logits.argmax(dim=-1)
        mask = torch.ones_like(data.y, dtype=torch.bool)
        total_correct += (pred[mask] == data.y[mask]).sum().item()
        total_nodes += mask.sum().item()
    acc = total_correct / max(1, total_nodes)
    return acc

# ---------------------------
# Main (example)
# ---------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=str, required=True,
                        help="CSV manifest listing OAS/SAbDab samples and file paths.")
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--hidden", type=int, default=512)
    parser.add_argument("--layers", type=int, default=6)
    parser.add_argument("--heads", type=int, default=8)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--weight_decay", type=float, default=1e-2)
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--spatial_topk", type=int, default=16)
    parser.add_argument("--spatial_threshold", type=float, default=None)
    parser.add_argument("--num_node_classes", type=int, default=2)
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Dataset
    dataset = AntibodyGraphDataset(
        manifest_csv=args.manifest,
        add_sequential_edges=True,
        spatial_topk=args.spatial_topk,
        spatial_threshold=args.spatial_threshold,
        use_rbf_edge_attr=True,
        rbf_K=16
    )

    # Simple split (中文：演示用简易划分)
    n = len(dataset)
    n_train = int(0.8 * n)
    n_val = n - n_train
    train_set, val_set = torch.utils.data.random_split(dataset, [n_train, n_val])

    train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=args.batch_size, shuffle=False)

    # Infer seq embedding dim from first sample
    sample = dataset[0]
    seq_dim = sample.x.size(-1)

    model = AntibodyGraphModel(
        seq_dim=seq_dim,
        hidden=args.hidden,
        edge_out_dim=64,
        heads=args.heads,
        layers=args.layers,
        dropout=args.dropout,
        num_node_classes=args.num_node_classes
    ).to(device)

    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    print(f"Train size: {len(train_set)}, Val size: {len(val_set)}, Seq dim: {seq_dim}")
    for epoch in range(1, args.epochs + 1):
        train_loss = train_epoch(model, train_loader, optimizer, device)
        val_acc = evaluate(model, val_loader, device)
        print(f"[Epoch {epoch:02d}] train_loss={train_loss:.4f}  val_acc={val_acc:.4f}")

    # 保存模型（中文：保存训练好的权重）
    torch.save(model.state_dict(), "antibody_graph_transformer.pt")
    print("Saved model to antibody_graph_transformer.pt")

if __name__ == "__main__":
    main()
How to prepare your data (quick guide)
1) OAS sequence embeddings

Use a protein LM (e.g., ESM-2 or AntiBERTy) to embed each residue.

Save each chain embedding as .npy with shape [L, D_seq].

Tip（中文）：注意与SAbDab序列对齐（ANARCI编号有助于稳定对应关系）。

2) SAbDab structure coordinates

Parse PDB and extract Cα per residue for each chain.

Save as .npy with shape [L, 3].

The dataset class builds spatial edges (topk or threshold) from these coordinates.

3) Manifest CSV example

csv
Copy
Edit
id,source,seq_emb_path,coords_path,aa_idx_path,label_path
7FAB_H,SAbDab,/data/oas_emb/7FAB_H.npy,/data/sabdab_ca/7FAB_H.npy,,/data/labels/7FAB_H_nodes.npy
7FAB_L,SAbDab,/data/oas_emb/7FAB_L.npy,/data/sabdab_ca/7FAB_L.npy,,
OAS_1234,OAS,/data/oas_emb/OAS_1234.npy,,,
source is optional (used for logging).

label_path is optional (node-level in this template). You can switch to graph-level by changing the head + loss.

Adapting to your tasks
Node-level paratope: keep as-is (labels per residue 0/1).

Graph-level property (e.g., affinity):

Replace node_head with graph head:

python
Copy
Edit
g = global_mean_pool(h, data.batch)  # [B, H]
logits = self.graph_head(g)          # regression or classification
Use MSE/Huber for regression; CE for classification.

Self-supervised pretraining (中文：自监督预训练):

Add masked residue modeling (mask some aa_idx and predict).

Add distance prediction for sampled residue pairs (only for SAbDab).

Add sequence↔graph contrastive (align global seq embedding with pooled graph).

If you’d like, I can also generate a tiny synthetic manifest + dummy .npy files to prove the pipeline runs end-to-end on your machine, or extend this to multi-chain graphs (VH+VL) with inter-chain edges.









Ask ChatGPT
