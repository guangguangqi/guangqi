from sklearn.svm import SVC
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# 加载数据
X, y = load_iris(return_X_y=True)

# 训练/测试集划分
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 构建 SVC 模型
clf = SVC(kernel='rbf', probability=True)
clf.fit(X_train, y_train)

# 预测标签
y_pred = clf.predict(X_test)  # 输出: int 数组

# 预测概率
proba = clf.predict_proba(X_test)  # 输出: float 数组，每类的概率

# 决策函数输出
scores = clf.decision_function(X_test)  # 输出: 距离边界的分数
