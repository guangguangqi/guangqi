from skopt import gp_minimize
from skopt.space import Real
from skopt.utils import use_named_args

# 定义目标函数（如优化 SVM 的 C 和 gamma）
def objective(params):
    C, gamma = params
    model = SVC(C=C, gamma=gamma)
    model.fit(X_train, y_train)
    return -model.score(X_test, y_test)  # 目标是最大化准确率，最小化负值

# 定义搜索空间
space = [Real(1e-6, 1e+6, name='C'),
         Real(1e-6, 1e+1, name='gamma')]

# 运行贝叶斯优化
res = gp_minimize(objective, space, n_calls=20, random_state=42)

# 输出最优参数
print(f"最优参数: C={res.x[0]}, gamma={res.x[1]}")
print(f"最优得分: {-res.fun}")
