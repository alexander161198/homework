import numpy as np
import matplotlib.pyplot as plt

def l_i(i,x,x_nodes):
    baz_polinom = 1.
    for j in range (len(x_nodes)):
        if i!=j:
            baz_polinom = baz_polinom*((x-x_nodes[j])/(x_nodes[i]-x_nodes[j]))
    return baz_polinom


def L(x, x_nodes, y_nodes):
    inter_polinom = 0
    for j in range (len(x_nodes)):
        inter_polinom = inter_polinom + y_nodes[j]*l_i(j,x,x_nodes)
    return inter_polinom
    

def first_func (x, a, b, m, n):
    num = 0.
    denom = 1.
    
    for j in range (m+1):
        num = num + a[j]*(x**j)
    for k in range (1,n+1):
        denom = denom + b[k-1]*(x**k)
        
    return (num/denom)


def cheb_nodes (n):
    cheb_array=np.zeros(n)
    for i in range (1,n+1):
        cheb_array[i-1] = np.cos(((2*i-1)/(2*n))*np.pi)
    return cheb_array



num_nodes = 5                       #число узлов
num_show = 4                        #число функций, выведенных на экран
x = np.linspace(-1., 1., 100, endpoint=True)
x_lagr = np.linspace(-1., 1., num_nodes, endpoint=True)

a = []
b = []
m = np.random.randint(7, 16, 100)
n = np.random.randint(7, 16, 100)

for i in range (100):
    a.insert(i, np.random.sample(m[i]+1))
    b.insert(i, np.random.sample(n[i]))


norm_cheb=np.zeros((num_show,30))
norm_lagr=np.zeros((num_show,30)) 

for i in range (num_show):    
    func_lagr = first_func (x_lagr, a[i], b[i], m[i], n[i])
    func_cheb = first_func (cheb_nodes(num_nodes), a[i], b[i], m[i], n[i])
    
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(8, 6), dpi=100)
    axes.plot(x, first_func(x, a[i], b[i], m[i], n[i]), color="blue", label="Функция")
    axes.plot(x, L(x,x_lagr, func_lagr), color="red", label="Равномерные узлы")
    axes.plot(x_lagr, func_lagr,'o', color="red")
    axes.plot(x, L(x, cheb_nodes(num_nodes), func_cheb), color="black", label="Чебышевские узлы")
    axes.plot(cheb_nodes(num_nodes), func_cheb,'o', color="black")
    axes.set_xlabel('x')
    axes.set_ylabel('f(x)')
    axes.legend()
    axes.grid()
    plt.show()
   
    
    for j in range (1,31):    
        x_check = np.linspace(-1., 1., j, endpoint=True)
        polinom_lagr = L(x, x_check, first_func(x_check, a[i], b[i], m[i], n[i]))
        f_value = first_func(x, a[i], b[i], m[i], n[i])
        polinom_cheb = L(x, cheb_nodes(j), first_func(cheb_nodes(j), a[i], b[i], m[i], n[i]))
        
        norm_lagr[i][j-1] = np.max(np.abs(polinom_lagr - f_value))
        norm_cheb[i][j-1] = np.max(np.abs(polinom_cheb - f_value))


    xs = np.arange(1,31)
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(8, 6), dpi=100)
    axes.semilogy(xs, norm_lagr[i], color="blue", label="равномерные узлы" )
    axes.semilogy(xs, norm_cheb[i], color="red", label="чебышевские узлы")
    axes.set_xlabel('Число узлов N')
    axes.set_ylabel('Расстояние')
    axes.legend()
    axes.grid()
    plt.show()