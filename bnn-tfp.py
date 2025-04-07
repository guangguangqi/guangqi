import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.keras import layers

tfd = tfp.distributions

# 构建贝叶斯神经网络模型
def create_bnn_model(input_dim):
    model = tf.keras.Sequential([
        tfp.layers.DenseFlipout(64, activation='relu', input_shape=(input_dim,)),
        tfp.layers.DenseFlipout(64, activation='relu'),
        tfp.layers.DenseFlipout(1)  # 输出均值
    ])
    return model

# 自定义损失函数：负对数似然（NLL）+ KL 散度
def nll(y_true, y_pred):
    dist = tfd.Normal(loc=y_pred, scale=1.0)
    return -tf.reduce_mean(dist.log_prob(y_true))

# 构建模型并编译
model = create_bnn_model(input_dim=10)
model.compile(optimizer='adam', loss=nll)

# 假设 X_train 和 y_train 是 shape 为 [N, 10] 和 [N, 1] 的张量
# model.fit(X_train, y_train, epochs=100)
