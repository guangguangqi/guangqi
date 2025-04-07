import tensorflow as tf
import numpy as np

# 假设状态是一个 4 维向量
state_dim = 4
action_dim = 2  # 动作有两个（离散）：0 或 1

# 创建一个示例状态输入（float32）
state = tf.constant([[0.1, -0.2, 0.05, 0.3]], dtype=tf.float32)  # shape: [1, 4]

# 创建一个简单的策略网络（Policy Network）
class PolicyNetwork(tf.keras.Model):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.dense1 = tf.keras.layers.Dense(128, activation='relu')
        self.logits = tf.keras.layers.Dense(action_dim)  # 输出 logits，未加 softmax

    def call(self, x):
        x = self.dense1(x)
        return self.logits(x)

# 初始化策略网络
policy_net = PolicyNetwork(state_dim, action_dim)

# 前向传播，获取动作 logits
logits = policy_net(state)  # shape: [1, action_dim]
action_probs = tf.nn.softmax(logits)

# 从概率分布中采样一个动作
action_dist = tf.random.categorical(logits, num_samples=1)  # shape: [1, 1]
action = tf.squeeze(action_dist)  # 去掉多余维度，变成标量

# 假设一个奖励值
reward = tf.constant(1.0, dtype=tf.float32)

# 创建一个简单的 Q 网络（输出每个动作的 Q 值）
class QNetwork(tf.keras.Model):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.dense1 = tf.keras.layers.Dense(128, activation='relu')
        self.q_values = tf.keras.layers.Dense(action_dim)

    def call(self, x):
        x = self.dense1(x)
        return self.q_values(x)

# 初始化 Q 网络
q_net = QNetwork(state_dim, action_dim)
q_values = q_net(state)  # shape: [1, action_dim]

# 打印输出
print("输入状态：", state.numpy())
print("输出动作概率：", action_probs.numpy())
print("选中的动作：", int(action.numpy()))
print("奖励值：", float(reward.numpy()))
print("Q 值（每个动作）：", q_values.numpy())
