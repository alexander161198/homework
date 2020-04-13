import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm as tr

def poly_regression(x_nodes, y_nodes, degree):
    #return np.polyfit(x_nodes,y_nodes,degree)

    n = len(x_nodes)
    sum_x = np.zeros(2*degree)
    sum_xy = np.zeros(degree+1)
    
    for i in range (2*degree):
        sum_x[i] = sum(x_nodes**(i+1))
        
    for i in range (degree+1):
        sum_xy[i] = sum(y_nodes*x_nodes**i)
        
    A = np.zeros((degree+1,degree+1))
    for i in range (degree+1):
        for j in range (degree+1):
            A[i][j] = sum_x[(2*degree-1)-i-j]
    A[degree][degree] = n
    
    B = np.zeros(degree+1)
    for i in range (degree+1):
        B[i] = sum_xy[degree-i]

    X = np.linalg.inv(A).dot(B)
    return X


def get_y (x, X, sigma):
    y = [-10*(x[i]**2) + 1.5*x[i] + 1 + sigma*X[i] for i in range(len(x))]
    return y

    
def draw_graph (coeffs, x_r, y_r, x_t, y_t):
    x_poly = np.linspace (-1, 1, 200)
    y_poly = np.polyval(coeffs, x_poly)
    plt.figure(1, figsize=(15, 10))
    plt.xlabel('x', size = 18)
    plt.ylabel('y', size = 18)
    plt.grid()
    plt.plot(x_poly, y_poly, color = "red", linewidth = 4, label = "полученный многочлен")
    plt.scatter(x_r, y_r, color = 'black', label='начальный набор данных Dregr')
    plt.scatter(x_t, y_t, color = 'blue', label='проверочный набор данных Dtest')
    plt.legend(fontsize="x-large")
    plt.show

def get_pogr (x_nodes, y_nodes, coeffs) :
    y_new = np.polyval(coeffs, x_nodes)
    sum = 0
    for i in range(len(y_nodes)) :
        sum += (y_nodes[i] - y_new[i]) ** 2
    return (sum/len(y_nodes)) ** (.5)


sigma = []
N = []
p = []
for i in range (5):
    sigma.insert(i,10**(i-2))
    p.insert(i,i+1)
for i in range (7):
    N.insert(i,2**(i+3))
print(N[4])

x=[]
X=[]
pogr_regr=[]
pogr_test=[]
pogr_otn=[]

for i in range (len(N)):
    x_regr = np.random.uniform(-1, 1, N[i])
    x_test = np.random.uniform(-1, 1, N[i])
    X_regr = [tr.rvs(-1, 1) for i in range(N[i])]
    X_test = [tr.rvs(-1, 1) for i in range(N[i])]
    y_regr = get_y(x_regr, X_regr, 1)               #sigma=1
    y_test = get_y(x_test, X_test, 1)
    coeffs = poly_regression(x_regr, y_regr, 2)     #p=3
    if (i == 4):
        draw_graph(coeffs, x_regr, y_regr, x_test, y_test)
    pogr_regr.append(get_pogr(x_regr, y_regr, coeffs))
    pogr_test.append(get_pogr(x_test, y_test, coeffs))
    pogr_otn.append((np.abs((-10 - coeffs[0]) / -10) + np.abs((1.5 - coeffs[1]) / 1.5) + np.abs(1 - coeffs[2])) / 3)

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(8, 6), dpi=100)
axes.plot(N, pogr_regr, color="blue", label="начальный набор данных" )
axes.plot(N, pogr_test, color="red", label="проверочный набор данных")
axes.set_xlabel('количество узлов N')
axes.set_ylabel('среднеквадратичная погрешность')
axes.legend()
axes.grid()
plt.show()


fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(8, 6), dpi=100)
axes.plot(N, pogr_otn, color="green")
axes.set_xlabel('количество узлов N')
axes.set_ylabel('относительная погрешность')
axes.grid()
plt.show()

pogr_regr=[]
pogr_test=[]

for i in range (len(p)) :
    x_regr = np.random.uniform(-1, 1, N[4])
    x_test = np.random.uniform(-1, 1, N[4])
    X_regr = [tr.rvs(-1, 1) for i in range(N[4])]
    X_test = [tr.rvs(-1, 1) for i in range(N[4])]
    y_regr = get_y(x_regr, X_regr, 10)               #sigma=1
    y_test = get_y(x_test, X_test, 10)
    coeffs = poly_regression(x_regr, y_regr, p[i])

    pogr_regr.append(get_pogr(x_regr, y_regr, coeffs))
    pogr_test.append(get_pogr(x_test, y_test, coeffs))
    
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(8, 6), dpi=100)
axes.plot(p, pogr_regr, color="blue", label="начальный набор данных" )
axes.plot(p, pogr_test, color="red", label="проверочный набор данных")
axes.set_xlabel('степень полинома p')
axes.set_ylabel('среднеквадратичная погрешность')
axes.legend()
axes.grid()
plt.show()

num = 0
pogr_otn=[]
for i in range (len(sigma)) :
    x_regr = np.random.uniform(-1, 1, N[2])
    X_regr = [tr.rvs(-1, 1) for i in range(N[2])]
    y_regr = get_y(x_regr, X_regr, sigma[i])
    coeffs = poly_regression(x_regr, y_regr, 3)     #p=3
    pogr_otn.append((np.abs((-10 - coeffs[0]) / -10) + np.abs((1.5 - coeffs[1]) / 1.5) + np.abs(1 - coeffs[2])) / 3)
    num += 1
  
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(8, 6), dpi=100)
axes.plot(N[:num], pogr_otn, color="green")
axes.set_xlabel('количество узлов N')
axes.set_ylabel('относительная погрешность')
axes.grid()
plt.show()