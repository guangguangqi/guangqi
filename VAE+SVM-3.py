# 用 VAE + SVM 做异常检测（科学时序数据）
import numpy as np

# 模拟正常数据：正弦信号 + 噪声
def generate_normal(n_samples=1000, seq_len=100, channels=3):
    t = np.linspace(0, 2*np.pi, seq_len)
    data = np.stack([
        np.sin(t + np.random.rand()) + 0.1 * np.random.randn(seq_len)
        for _ in range(n_samples * channels)
    ], axis=0).reshape(n_samples, seq_len, channels)
    return data

# 模拟异常数据：叠加突变
def generate_anomaly(n_samples=200, seq_len=100, channels=3):
    normal = generate_normal(n_samples, seq_len, channels)
    anomaly = normal.copy()
    anomaly[:, 20:30, :] += np.random.uniform(3, 5)  # 注入异常
    return anomaly

X_normal = generate_normal()
X_anomaly = generate_anomaly()

# 合并
X_all = np.concatenate([X_normal, X_anomaly], axis=0)
y_all = np.array([0]*len(X_normal) + [1]*len(X_anomaly))  # 0: 正常，1: 异常

# 归一化
X_all = (X_all - np.mean(X_all)) / np.std(X_all)

########构建 VAE 模型（编码时序数据）
import tensorflow as tf
from tensorflow.keras import layers, Model

input_shape = X_all.shape[1:]  # (时间步, 通道数)
latent_dim = 4

# 编码器
inputs = layers.Input(shape=input_shape)
x = layers.Conv1D(32, 3, activation='relu', padding='same')(inputs)
x = layers.MaxPooling1D(2)(x)
x = layers.Flatten()(x)
z_mean = layers.Dense(latent_dim)(x)
z_log_var = layers.Dense(latent_dim)(x)

def sampling(args):
    z_mean, z_log_var = args
    eps = tf.random.normal(shape=tf.shape(z_mean))
    return z_mean + tf.exp(0.5 * z_log_var) * eps

z = layers.Lambda(sampling)([z_mean, z_log_var])

# 解码器
decoder_input = layers.Input(shape=(latent_dim,))
x = layers.Dense((input_shape[0]//2) * 32, activation='relu')(decoder_input)
x = layers.Reshape((input_shape[0]//2, 32))(x)
x = layers.UpSampling1D(2)(x)
outputs = layers.Conv1D(input_shape[1], 3, activation='sigmoid', padding='same')(x)

encoder = Model(inputs, z_mean)
decoder = Model(decoder_input, outputs)
vae_output = decoder(z)

vae = Model(inputs, vae_output)

# 损失函数
recon_loss = tf.keras.losses.mse(inputs, vae_output)
recon_loss = tf.reduce_mean(recon_loss)
kl_loss = -0.5 * tf.reduce_mean(1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var))
vae_loss = recon_loss + kl_loss
vae.add_loss(vae_loss)
vae.compile(optimizer='adam')
vae.fit(X_normal, X_normal, epochs=30, batch_size=32, verbose=1)

###########提取潜在表示 z + 用 SVM 做异常检测
from sklearn.svm import OneClassSVM
from sklearn.metrics import classification_report

# 提取潜在空间表示
Z_all = encoder.predict(X_all)

# 使用 OneClassSVM 拟合正常数据
svm = OneClassSVM(kernel='rbf', nu=0.05, gamma='scale')
svm.fit(Z_all[y_all == 0])  # 只用正常样本训练

# 预测
y_pred = svm.predict(Z_all)
y_pred = (y_pred == -1).astype(int)  # -1 为异常 → 1

print(classification_report(y_all, y_pred))

### 可视化潜在空间（选做）
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

z_2d = PCA(n_components=2).fit_transform(Z_all)
plt.scatter(z_2d[:, 0], z_2d[:, 1], c=y_all, cmap='coolwarm', s=15)
plt.title("VAE 潜在空间中的正常 / 异常分布")
plt.xlabel("z1")
plt.ylabel("z2")
plt.colorbar(label='0=正常, 1=异常')
plt.show()
