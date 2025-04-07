###########构建并训练 VAE
from tensorflow.keras.layers import Input, Dense, Lambda
from tensorflow.keras.models import Model
from tensorflow.keras.losses import binary_crossentropy
import tensorflow as tf
import numpy as np
from sklearn.svm import SVC
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

# 加载只包含数字 0 和 1 的样本
digits = load_digits(n_class=2)
X = digits.data / 16.0  # 归一化
y = digits.target       # 标签：0 或 1

# 分割训练测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

input_dim = X.shape[1]
latent_dim = 2  # 压缩到二维，便于可视化

# Encoder
inputs = Input(shape=(input_dim,))
h = Dense(64, activation='relu')(inputs)
z_mean = Dense(latent_dim)(h)
z_log_var = Dense(latent_dim)(h)

# 采样函数
def sampling(args):
    z_mean, z_log_var = args
    epsilon = tf.random.normal(shape=(tf.shape(z_mean)[0], latent_dim))
    return z_mean + tf.exp(0.5 * z_log_var) * epsilon

z = Lambda(sampling)([z_mean, z_log_var])

# Decoder
decoder_h = Dense(64, activation='relu')
decoder_out = Dense(input_dim, activation='sigmoid')
h_decoded = decoder_h(z)
outputs = decoder_out(h_decoded)

# VAE 模型
vae = Model(inputs, outputs)

# VAE 损失函数
recon_loss = binary_crossentropy(inputs, outputs)
recon_loss = tf.reduce_mean(recon_loss * input_dim)
kl_loss = -0.5 * tf.reduce_mean(1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var))
vae_loss = recon_loss + kl_loss
vae.add_loss(vae_loss)
vae.compile(optimizer='adam')
vae.fit(X_train, X_train, epochs=50, batch_size=32, verbose=0)

###########从 Encoder 提取潜在向量 z
# 定义 Encoder 模型
encoder = Model(inputs, z_mean)
z_train = encoder.predict(X_train)
z_test = encoder.predict(X_test)
##############用潜在向量 z 训练 SVM 分类器
svm = SVC(kernel='rbf')
svm.fit(z_train, y_train)

# 测试分类性能
acc = svm.score(z_test, y_test)
print(f"VAE 编码器 + SVM 分类准确率：{acc:.2f}")
###############可视化潜在空间
import matplotlib.pyplot as plt

z_all = encoder.predict(X)
plt.scatter(z_all[:, 0], z_all[:, 1], c=y, cmap='coolwarm', s=30)
plt.title("VAE 编码器输出的潜在空间 z")
plt.xlabel("z1")
plt.ylabel("z2")
plt.grid(True)
plt.colorbar(label='类别')
plt.show()
