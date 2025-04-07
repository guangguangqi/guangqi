from sklearn.svm import SVC, SVR
import numpy as np

# 分类输入
X_cls = np.array([[1.0, 2.0], [1.5, 1.8], [2.0, 2.2]])
y_cls = np.array([0, 0, 1])

svc = SVC(probability=True)
svc.fit(X_cls, y_cls)
print("分类预测：", svc.predict(X_cls))            # int 类型输出
print("预测概率：", svc.predict_proba(X_cls))      # float 类型输出

# 回归输入
X_reg = np.array([[1], [2], [3]])
y_reg = np.array([2.0, 3.5, 6.1])

svr = SVR()
svr.fit(X_reg, y_reg)
print("回归预测：", svr.predict(X_reg))            # float 输出
