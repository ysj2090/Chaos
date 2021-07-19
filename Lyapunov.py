import numpy as np
import matplotlib.pyplot as plt


def logistic(r, x):
    return r * x * (1 - x)


# 관측할 r과 각 r의 상태 x 생성
n = 10000
r = np.linspace(2.5, 4.0, n)
x = 0.1 * np.ones(n)

# step 수 및 diagram에 나타낼 state 개수(last) 설정
step = 1000
last = 100

# r에 따른 Lyapunov exponents 설정
lyapunov = np.zeros(n)

fig = plt.figure()
subplot = fig.add_subplot(2, 1, 1)
for n in range(step):
    x = logistic(r, x)
    # Lyapunov exponents 계산
    lyapunov += np.log(abs(r - 2 * r * x))
#    print(n, 'Lyapunov=', lyapunov)
    # 각 r에 대한 마지막 100개의 상태 x 플롯
    if n >= (step - last):
        plt.plot(r, x, marker=',', ls='', c='black', alpha=0.2)
lyapunov = lyapunov / step
plt.xlim(2.5, 4)
plt.title("Bifurcation diagram")
plt.xlabel('r')
plt.ylabel('x')
subplot = fig.add_subplot(2, 1, 2)
plt.plot(r, lyapunov, marker=',', ls='', c='black', alpha=0.2)
plt.axhline(y=0, c='red')
plt.xlim(2.5, 4)
plt.title("Lyapunov exponent")
plt.tight_layout()
plt.show()
