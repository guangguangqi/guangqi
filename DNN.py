import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical

# 1️⃣ 加载数据
data = load_iris()
X = data['data']            # shape: [150, 4]
y = data['target']          # 标签：0,1,2

# 标准化特征
X = StandardScaler().fit_transform(X)

# one-hot 编码标签
y_cat = to_categorical(y, num_classes=3)

# 分割训练和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2, random_state=42)

# 2️⃣ 构建 DNN 模型
latent_dim = 2  # 潜在空间维度，用于可视化

model = models.Sequential([
    layers.Input(shape=(4,)),
    layers.Dense(16, activation='relu'),
    layers.Dense(latent_dim, name="latent_space"),  # 潜在空间
    layers.Dense(3, activation='softmax')           # 3 类分类
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=50, batch_size=8, validation_split=0.1, verbose=0)

# 3️⃣ 提取潜在空间的表示
extractor = models.Model(inputs=model.input, outputs=model.get_layer("latent_space").output)
latent_features = extractor.predict(X)  # shape: [150, 2]

# 4️⃣ 可视化潜在空间（2D）
plt.figure(figsize=(8, 6))
for i in range(3):
    idx = (y == i)
    plt.scatter(latent_features[idx, 0], latent_features[idx, 1], label=f'Class {i}', s=40)
plt.title("Iris 数据的 DNN 潜在空间可视化")
plt.xlabel("潜在维度 1")
plt.ylabel("潜在维度 2")
plt.legend()
plt.grid(True)
plt.show()
