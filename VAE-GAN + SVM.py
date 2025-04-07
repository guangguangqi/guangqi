####1 VAE-GAN 编码器 + 判别器 D + SVM 检测器
X_normal = generate_normal(n_samples=1000)
X_anomaly = generate_anomaly(n_samples=200)
X_all = np.concatenate([X_normal, X_anomaly])
y_all = np.array([0]*len(X_normal) + [1]*len(X_anomaly))

#####2 构建 VAE-GAN 网络（编码器 + 解码器 + 判别器）
from tensorflow.keras import layers, Model

# 编码器（Encoder）
def build_encoder(input_shape, latent_dim=4):
    inputs = layers.Input(shape=input_shape)
    x = layers.Conv1D(32, 3, activation='relu', padding='same')(inputs)
    x = layers.MaxPooling1D(2)(x)
    x = layers.Flatten()(x)
    z_mean = layers.Dense(latent_dim)(x)
    z_log_var = layers.Dense(latent_dim)(x)
    return Model(inputs, [z_mean, z_log_var])

# 重参数采样
def sampling(z_mean, z_log_var):
    epsilon = tf.random.normal(shape=tf.shape(z_mean))
    return z_mean + tf.exp(0.5 * z_log_var) * epsilon

# 解码器（Decoder / Generator）
def build_decoder(output_shape, latent_dim):
    latent_inputs = layers.Input(shape=(latent_dim,))
    x = layers.Dense((output_shape[0]//2) * 32, activation='relu')(latent_inputs)
    x = layers.Reshape((output_shape[0]//2, 32))(x)
    x = layers.UpSampling1D(2)(x)
    outputs = layers.Conv1D(output_shape[1], 3, activation='sigmoid', padding='same')(x)
    return Model(latent_inputs, outputs)

# 判别器（Discriminator）
def build_discriminator(input_shape):
    inputs = layers.Input(shape=input_shape)
    x = layers.Conv1D(32, 3, activation='relu', padding='same')(inputs)
    x = layers.Flatten()(x)
    x = layers.Dense(64, activation='relu')(x)
    out = layers.Dense(1, activation='sigmoid')(x)
    return Model(inputs, out)

###########3 构建训练循环（VAE loss + GAN loss）
# 初始化模块
latent_dim = 4
input_shape = X_normal.shape[1:]

encoder = build_encoder(input_shape, latent_dim)
decoder = build_decoder(input_shape, latent_dim)
discriminator = build_discriminator(input_shape)

optimizer = tf.keras.optimizers.Adam(1e-4)
bce = tf.keras.losses.BinaryCrossentropy()

@tf.function
def train_step(x_batch):
    with tf.GradientTape(persistent=True) as tape:
        z_mean, z_log_var = encoder(x_batch)
        z = sampling(z_mean, z_log_var)
        x_recon = decoder(z)

        # VAE loss
        recon_loss = tf.reduce_mean(tf.keras.losses.mse(x_batch, x_recon))
        kl_loss = -0.5 * tf.reduce_mean(1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var))
        vae_loss = recon_loss + kl_loss

        # GAN loss
        real_out = discriminator(x_batch)
        fake_out = discriminator(x_recon)
        d_loss = bce(tf.ones_like(real_out), real_out) + bce(tf.zeros_like(fake_out), fake_out)
        g_loss = bce(tf.ones_like(fake_out), fake_out)

        total_loss = vae_loss + 0.1 * g_loss

    # 更新参数
    grads_enc = tape.gradient(total_loss, encoder.trainable_weights)
    grads_dec = tape.gradient(total_loss, decoder.trainable_weights)
    grads_d   = tape.gradient(d_loss, discriminator.trainable_weights)

    optimizer.apply_gradients(zip(grads_enc, encoder.trainable_weights))
    optimizer.apply_gradients(zip(grads_dec, decoder.trainable_weights))
    optimizer.apply_gradients(zip(grads_d, discriminator.trainable_weights))

    return total_loss, d_loss

# 训练
X_train = X_normal  # 只用正常数据训练
for epoch in range(30):
    loss, d_loss = train_step(tf.convert_to_tensor(X_train.astype("float32")))
    print(f"Epoch {epoch+1}, VAE-GAN Loss: {loss:.4f}, D Loss: {d_loss:.4f}")

######4️⃣ 提取 z 并训练 SVM
Z_all = encoder.predict(X_all)[0]  # 取均值作为 z
from sklearn.svm import OneClassSVM
from sklearn.metrics import classification_report

svm = OneClassSVM(nu=0.05, kernel='rbf', gamma='scale')
svm.fit(Z_all[y_all == 0])  # 只用正常数据拟合

# 预测
y_pred = svm.predict(Z_all)
y_pred = (y_pred == -1).astype(int)

print(classification_report(y_all, y_pred))

########
