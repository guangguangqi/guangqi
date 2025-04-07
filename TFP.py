import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.keras import layers

# 输入数据
x = tf.constant([[1.0, 2.0], [3.0, 4.0]], dtype=tf.float32)  # shape: [2, 2]

# 贝叶斯密集层：输出正态分布（用于回归）
model = tf.keras.Sequential([
    tfp.layers.DenseFlipout(1 + 1)  # 输出均值 + log 方差
])

# 输出是正态分布的参数
output = model(x)
mean, log_var = tf.split(output, num_or_size_splits=2, axis=-1)
stddev = tf.exp(0.5 * log_var)

# 构建概率分布对象
distribution = tfp.distributions.Normal(loc=mean, scale=stddev)

# 打印输出
print("预测均值：", mean.numpy())
print("预测标准差：", stddev.numpy())
