import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# 创建一个包含负值和正值的数组
x = tf.constant(np.linspace(-10, 10, 100), dtype=tf.float32)

# 使用 ReLU 激活函数
y = tf.nn.relu(x)

# 可视化
plt.plot(x, y)
plt.title("ReLU 激活函数")
plt.xlabel("输入 x")
plt.ylabel("输出 ReLU(x)")
plt.grid(True)
plt.show()
