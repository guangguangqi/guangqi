from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
import numpy as np

# 输入数据
X_train = np.array([[1.0], [2.0], [3.0]])
y_train = np.array([1.5, 1.8, 2.1])

# 测试输入
X_test = np.array([[1.5], [2.5]])

# 定义 GP 模型
gp = GaussianProcessRegressor(kernel=RBF(), alpha=1e-2)
gp.fit(X_train, y_train)

# 输出预测结果：mean 和 std（方差）
y_mean, y_std = gp.predict(X_test, return_std=True)

print("输入 X_test：", X_test)
print("预测均值：", y_mean)     # float 数组
print("预测标准差：", y_std)   # float 数组
