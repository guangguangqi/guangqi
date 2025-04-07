from sklearn.ensemble import RandomForestClassifier
import numpy as np

# 输入特征（float 类型的二维数组）
X = np.array([
    [5.1, 3.5, 1.4, 0.2],
    [7.0, 3.2, 4.7, 1.4],
    [6.3, 3.3, 6.0, 2.5]
])

# 标签（整数类别）
y = np.array([0, 1, 2])

# 初始化模型并训练
model = RandomForestClassifier()
model.fit(X, y)

# 预测
pred_class = model.predict(X)          # int 数组：如 [0, 1, 2]
pred_proba = model.predict_proba(X)    # float 数组：如 [[0.9, 0.1, 0.0], ...]

print("预测类别：", pred_class)
print("预测概率：", pred_proba)
