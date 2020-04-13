import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""N-1 x 4"""
def qubic_spline_coeff(x_nodes, y_nodes):
    a = y_nodes
    h = x_nodes[1:] - x_nodes[:-1]
    
    """A*c=B"""
    A = np.diag(h, 1) + np.diag(h, -1) 
    for i in range (1, len(h)):
        A[i][i] = 2*(h[i]+h[i-1])
    A[0][0] = 1
    A[0][1] = 0
    A[-1][-1] = 1
    A[-1][-2] = 0
    
    B = np.zeros(len(x_nodes))
    for i in range (len(x_nodes)-2):
        B[i+1] = (3/h[i+1])*(a[i+2]-a[i+1]) - (3/h[i])*(a[i+1]-a[i])
    
    c = np.linalg.inv(A).dot(B)
    
    """searching "b" from formula (2.91)"""
    b = (1/h)*(a[1:]-a[:-1]) - (h/3)*(c[1:]+2*c[:-1])
    
    """searching "d" from formula (2.88)"""
    d = (c[1:]-c[:-1])/(3*h)
    
    coeffs = np.vstack((a[:-1], b, c[:-1], d))
    return coeffs
    
    
"""value of spline"""
def qubic_spline(x, qs_coeff, x_nodes):
    for i in range (len(x_nodes)-1):
        if (x < x_nodes[i+1] and x >= x_nodes[i]) or (x < x_nodes[i] and i==0):
            break
    a = qs_coeff[0][i]  
    b = qs_coeff[1][i]
    c = qs_coeff[2][i] 
    d = qs_coeff[3][i] 
    return a + b*(x-x_nodes[i]) + c*((x-x_nodes[i])**2) + d*((x-x_nodes[i])**3)
    

"""value of derivative of spline"""
def d_qubic_spline(x, qs_coeff, x_nodes):
    for i in range (len(x_nodes)):
        if (x < x_nodes[i+1] and x >= x_nodes[i]) or (x < x_nodes[i] and i==0):
            break
    a = qs_coeff[0][i]
    b = qs_coeff[1][i]
    c = qs_coeff[2][i] 
    d = qs_coeff[3][i] 
    return b + 2*c*(x-x_nodes[i]) + 3*d*((x-x_nodes[i])**2)


def plots (xs, y):
    qs_coeff = qubic_spline_coeff(xs, y)
    x_new = np.linspace(np.min(xs), np.max(xs), 1000)
    y_new = [qubic_spline(i, qs_coeff, xs) for i in x_new]
    
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 6), dpi=100)
    axes.plot(xs, y, 'o', x_new, y_new )
    axes.set_title("Температура в Ла-пасе в июне 2018")
    axes.set_xlabel('Число месяца')
    axes.set_ylabel('Температура, градусы Цельсия')
    axes.grid()
    plt.show()
    

"""for 6 step"""
def checking_dist (num):                
    counts=np.arange(1, len(xs)-1, num)
    x_check = np.delete(xs,counts)
    y_check = np.delete(y,counts)
    qs_coeff = qubic_spline_coeff(xs[1::num], y[1::num])
    y_new = [qubic_spline(i, qs_coeff, xs[1::num]) for i in x_check]
    norm=np.max(np.abs(y_new-y_check))
    return norm

"""for 6 step"""
def daily_temp (num):
    qs_coeff = qubic_spline_coeff(xs[1::num], y[1::num])
    y_new = [qubic_spline(i, qs_coeff, xs[1::num]) for i in xs]
    daily= np.zeros(30)
    for i in range (len(xs)):
        k = (int)(i/8)
        daily[k] = daily[k] + y_new[i]
    return np.max(daily/8)



file = pd.read_csv('la-paz.csv', sep=';', header = 6)

y = file['Местное время в Ла-Пасе / Эль-Альто (аэропорт)'][::-1]
y = y.values
len_time = len(y)

xs = np.linspace(1., 30., len_time)

plots (xs, y)                   #Every 3 hours
plots (xs[1::2], y[1::2])       #Every 6 hours
plots (xs[1::4], y[1::4])       #Every 12 hours
plots (xs[1::8], y[1::8])       #Every 24 hours

"""distance check"""
dist = np.zeros(2)
dist[0]=checking_dist(2)
dist[1]=checking_dist(4)

print(dist)

"""daily average check"""
daily = np.zeros(30)
daily_dist = np.zeros(len(dist))

for i in range (len(xs)):
    k = (int)(i/8)
    daily[k] = daily[k] + y[i]
daily=daily/8

daily_dist[0] = np.abs(np.max(daily - daily_temp(2)))
daily_dist[1] = np.abs(np.max(daily - daily_temp(4)))

print(daily_dist)
