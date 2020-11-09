
import numpy as np
from scipy.stats import multivariate_normal
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm





def f(x, mu = np.ones(2), cov = np.eye(2)):
    return multivariate_normal.pdf(x, mean=mu, cov=cov)



mu2 = np.array([-1,0])
cov2 = np.array([[2,1],[1,2]])
mu3  = np.array([-3,1])
# f()
#
#
#
#
#
#
#
#
#
#
# import numpy as np
# import matplotlib.pyplot as plt
#
# distributions = [
#     {"type": np.random.normal, "kwargs": {"loc": -3, "scale": 2}},
#     {"type": np.random.uniform, "kwargs": {"low": 4, "high": 6}},
#     {"type": np.random.normal, "kwargs": {"loc": 2, "scale": 1}},
# ]
# coefficients = np.array([0.5, 0.2, 0.3])
# coefficients /= coefficients.sum()      # in case these did not add up to 1
# sample_size = 100000
#
# num_distr = len(distributions)
# data = np.zeros((sample_size, num_distr))
# for idx, distr in enumerate(distributions):
#     data[:, idx] = distr["type"](size=(sample_size,), **distr["kwargs"])
# random_idx = np.random.choice(np.arange(num_distr), size=(sample_size,), p=coefficients)
# sample = data[np.arange(sample_size), random_idx]
# plt.hist(sample, bins=100, density=True)
# plt.show()
# print(distributions)
#
#
#
# import matplotlib.pyplot as plt
# from scipy.stats import multivariate_normal
# cov2 = np.array([[2,1],[1,2]])
# mu2 = np.array([-1,0])
#
# x = np.linspace(0, 5, 10, endpoint=False)
# y = multivariate_normal.pdf(x, mean=mu2, cov=cov2);
#
# fig1 = plt.figure()
# ax = fig1.add_subplot(111)
# ax.plot(x, y)
#
#
#
# x=  np.linspace(0, 5, 10, endpoint=False)
# y= np.linspace(0, 5, 10, endpoint=False)
# mu = np.array([-1,0])
#
#
# def f(x, mu = np.ones(2), cov = np.eye(2)):
#     #print(x, mu, cov)
#     return multivariate_normal.pdf(x, mean=mu, cov=cov)
# #f((x,y), mu, .5* np.eye(2))
# f((5, 2), mu, cov2)
#
# #np.eye(2) * mu


num = 10
y=[]
#for i in range(0,num):
 #   y.append(f((2,1), mu, cov2))
#print(y)



cov5 = np.array([[2,1],[1,2]])
#f((-1,0),mu, cov5)



X = np.linspace(-5, 8, 10)


print(X)
print(X.reshape(-1,2))


X = np.linspace(-5, 8, 100)
Y = np.linspace(-5, 8, 100)
X, Y = np.meshgrid(X, Y)
print(X, Y)

# cov2 = np.array([[2,1],[1,2]])
# mu2 = np.array([-1,0])


X = np.linspace(-5, 5, 100)
Y = np.linspace(-5, 5, 100)

#X, Y = np.meshgrid(X, Y)
W = np.concatenate([X.reshape((-1, 1)), Y.reshape((-1,1))],axis=1)
#
mu1 = [np.array([1,1]), np.array([-1,0]), np.array([-3,1])]
cov1 = [np.array([[1,0],[0,1]]), np.array([[2,1],[1,2]]), np.array([[1,0],[0,1]])]
weights = (.2,.5,.3)
x_y =[[0,1], [-1,1],[1,0]]
#


Z = multivariate_normal.pdf(W, mean=np.array([1,1]), cov=np.array([[1,0],[0,1]]))
print(Z.reshape(-1,1))

Z = Z.reshape(-1,2)

#print(W)
print(Z)

#x_y = [0,1]
X = np.linspace(x_y[1][0], x_y[1][1], 100)
print(X)

def f(x, mu = np.ones(2), cov = np.eye(2)):
    return multivariate_normal.pdf(x, mean=mu, cov=cov)

def g(x_y, lst_mu, lst_cov, w, num):
    XYZ = []
    for i, w_ in enumerate(w):
        X = np.linspace(-x_y[i][0], x_y[i][1], int(num * w_))
        Y = np.linspace(-x_y[i][0], x_y[i][1], int(num * w_))
        XY = np.concatenate([X.reshape((-1, 1)), Y.reshape((-1, 1))], axis=1)
        Z = (multivariate_normal.pdf(XY, mean=lst_mu[i], cov=lst_cov[i]))
        XYZ_ = np.concatenate([XY, Z.reshape((-1,1))], axis=1)
        XYZ.append(XYZ_)
    return XYZ

XYZ1=g(x_y, mu1, cov1, weights, 100)

print(XYZ1)















