# 简单回归 BNN
import pyro
import pyro.distributions as dist
from pyro.nn import PyroModule, PyroSample
import torch
import torch.nn as nn

class BNN(PyroModule):
    def __init__(self):
        super().__init__()
        self.linear1 = PyroModule[nn.Linear](10, 64)
        self.linear1.weight = PyroSample(dist.Normal(0., 1.).expand([64, 10]).to_event(2))
        self.linear1.bias = PyroSample(dist.Normal(0., 1.).expand([64]).to_event(1))
        self.linear2 = PyroModule[nn.Linear](64, 1)
        self.linear2.weight = PyroSample(dist.Normal(0., 1.).expand([1, 64]).to_event(2))
        self.linear2.bias = PyroSample(dist.Normal(0., 1.).expand([1]).to_event(1))

    def forward(self, x, y=None):
        x = torch.relu(self.linear1(x))
        mean = self.linear2(x).squeeze(-1)
        sigma = 0.1  # 可以进一步建模为变量
        with pyro.plate("data", x.shape[0]):
            obs = pyro.sample("obs", dist.Normal(mean, sigma), obs=y)
        return mean
