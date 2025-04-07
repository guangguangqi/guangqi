import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.keras.layers import Dense, Dropout

# 输入张量
inputs = tf.keras.Input(shape=(20,))
x = Dense(64, activation='relu')(inputs)
x = Dropout(0.5)(x, training=True)  # 关键！保持训练模式，用于采样
x = Dense(64, activation='relu')(x)
x = Dropout(0.5)(x, training=True)
outputs = Dense(1)(x)  # 回归预测均值

model = tf.keras.Model(inputs, outputs)

# 多次前向传播获取不同预测
samples = [model(X_test, training=True) for _ in range(50)]
samples = tf.stack(samples, axis=0)  # shape: [50, batch_size, 1]

# 计算均值和标准差
pred_mean = tf.reduce_mean(samples, axis=0)
pred_std = tf.math.reduce_std(samples, axis=0)
