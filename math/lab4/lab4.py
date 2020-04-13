import numpy as np
import matplotlib.pyplot as plt
import lab3

font = {'size'   : 14}
plt.rc('font', **font)

N = lab3.N
M = lab3.M_new
num = (N-2)*(N-2)

def function (x):
    return 1 + np.dot(-M,x)


def ab4(h, f, T, i):
    brak = 55*f(T[i-1]) - 59*f(T[i-2]) + 37*f(T[i-3]) - 9*f(T[i-4])
    return T[i-1] + (h/24)*brak


def rk4(alpha, h, f):
    k = []
    k.append(h*f(alpha))
    k.append(h*f(alpha + 0.5*k[0]))
    k.append(h*f(alpha + 0.5*k[1]))
    k.append(h*f(alpha + k[2]))
    return alpha + (1/6)*(k[0]+2*k[1]+2*k[2]+k[3])


def plot_lines(T, i):
    T_plot = np.zeros((N, N))
    j = 0
    for l in range(N):
        for k in range(N):
            if (l > 0) and (l < N-1) and (k > 0) and (k < N-1):
                T_plot[l][k] = T[i][j]
                j += 1
                
    x = np.linspace(0, 1, N)
    y = np.linspace(0, 1, N)
    
    plt.figure(figsize=(10,6))
    plt.contourf(x, y, T_plot)
    plt.colorbar()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


def ode_solve(f, t_final, delta_t):
    time = t_final/delta_t
    time_vec = np.zeros((int(time),))
    
    for i in range (1, int(time)):
        time_vec[i] = time_vec[i-1] + delta_t
        
    T = np.zeros((int(time), num))
    T_average = np.zeros((int(time), ))
    
    for i in range (int(time)-1):
        if i<3:
            T[i+1] = rk4(T[i+1], delta_t, f)
        else:
            T[i+1] = ab4(delta_t, f, T, i+1)

    for i in range (1, len(T)):        
        T_average[i] = np.average(T[i])
        if (i == len(T)-1):
            plot_lines(T, i)
        
   # plt.figure(figsize=(10,6))    
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))
    axes.set_yscale('log')
    #plt.plot(time_vec, T_average)
    plt.plot(time_vec, T_average)
    plt.xlabel("время")
    plt.ylabel("усредненная температура")
    plt.grid()
    plt.show()
    
    return T



dt = 0.0001
t_final = 0.3
T_plot = np.zeros((int(t_final/dt), ))
ode_solve(function, t_final, dt)

