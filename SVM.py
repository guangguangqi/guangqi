import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.svm import SVC

# 1️⃣ 生成二维数据
X, y = make_classification(n_samples=200, n_features=2, n_redundant=0, 
                           n_informative=2, n_clusters_per_class=1, random_state=42)

# 2️⃣ 拟合 SVM 模型（RBF 核）
clf = SVC(kernel='rbf', C=1.0)
clf.fit(X, y)

# 3️⃣ 绘制决策边界
def plot_decision_boundary(clf, X, y):
    # 创建网格
    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 500),
                         np.linspace(y_min, y_max, 500))

    # 预测网格中所有点的类别
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # 绘制区域颜色
    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.3)

    # 绘制数据点
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm, s=30, edgecolors='k')

    # 绘制支持向量
    plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1],
                s=100, facecolors='none', edgecolors='black', linewidths=1.5, label='支持向量')

    plt.title("SVM 分类边界可视化")
    plt.xlabel("特征 1")
    plt.ylabel("特征 2")
    plt.legend()
    plt.grid(True)
    plt.show()

plot_decision_boundary(clf, X, y)
