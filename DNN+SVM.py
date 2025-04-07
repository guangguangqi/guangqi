import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.utils import to_categorical

# 加载数据
data = load_iris()
X = data['data']
y = data['target']

# 标准化
X = StandardScaler().fit_transform(X)

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#  构建并训练 DNN 特征提取器
# 构建 DNN 模型（不含最后一层 softmax）
input_dim = X.shape[1]
feature_model = Sequential([
    Input(shape=(input_dim,)),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(16, activation='relu', name='feature_layer')  # 特征层
])

# 编译模型，用分类目标做监督学习
x_in = Input(shape=(input_dim,))
x_feat = feature_model(x_in)
output = Dense(3, activation='softmax')(x_feat)
full_model = Model(inputs=x_in, outputs=output)

full_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
full_model.fit(X_train, y_train, epochs=100, verbose=0, batch_size=8)

# #
# 提取 DNN 中间层输出作为新特征
feature_extractor = Model(inputs=full_model.input, outputs=full_model.get_layer('feature_layer').output)

X_train_feat = feature_extractor.predict(X_train)
X_test_feat = feature_extractor.predict(X_test)

# 用提取的特征训练 SVM 分类器
svm = SVC(kernel='rbf', C=1.0)
svm.fit(X_train_feat, y_train)

###
acc = svm.score(X_test_feat, y_test)
print(f"DNN + SVM 测试集准确率：{acc:.2f}")

####
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_train_feat)

plt.figure(figsize=(8, 6))
for i in range(3):
    plt.scatter(X_pca[y_train == i, 0], X_pca[y_train == i, 1], label=f'Class {i}')
plt.title("DNN 提取的特征空间（PCA 降维）")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.legend()
plt.grid(True)
plt.show()
