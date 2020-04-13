import numpy as np
import matplotlib.pyplot as plt
import math
import sympy


def find_Ak(k, y_nodes):
   m = len(y_nodes)
   if (m == 2):
       return y_nodes[0] + y_nodes[1]*((-1)**k)
   Ok = find_Ak(k, y_nodes[1::2])
   Ek = find_Ak(k, y_nodes[::2])
   Ak = Ek + (math.e**(((-1j)*k*math.pi*2)/m))*Ok
   return Ak

    


def fft_coeff(y_nodes):
    #return np.fft.fft([float(i) for i in y_nodes])

   n = len(y_nodes)
   coeffs = []
   
   for k in range(n//2 + 1):
       Ak = find_Ak(k, y_nodes)
       Ak_coeff = (-1)**k / (2 * n)
       coeffs.append(Ak * Ak_coeff)
       
   return coeffs


def spectral_integral(f,N) :
    x_nodes = [(-math.pi + i * math.pi / N *2) for i in range (N)]
    y_nodes = []
    for i in x_nodes :
        y_nodes.append(f.subs(x,i))
    A = fft_coeff(y_nodes)
    y = 5 / 4 * math.pi * A[0].real / N
    for k in range (1, N):
        A[k] *= (-1) ** k / N
        y += 2 * A[k].real / k * math.sin(k * math.pi / 4)
        y -= 2 * A[k].imag / k * (math.cos(k * math.pi / 4) - math.cos(k * math.pi))
    return y


I=[]
y=[]
x = sympy.Symbol('x')
I.append(abs(x))
I.append(x * sympy.cos(x ** 2) + math.e ** x * sympy.cos(math.e ** x))
y.append(sympy.integrate(I[0], (x, -math.pi/4, math.pi)))
y.append(sympy.integrate(I[1], (x, -math.pi/4, math.pi)))
print (y)

N = [2**n for n in range (1, 9)]
pogr=np.zeros(len(N))

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 12), dpi=100) 
for j in range (len(I)) :
    for i in range (len(N)) :
        y_new = (spectral_integral(I[j], N[i]))
        if (i==6) :
            print (y_new)
        pogr[i] =  math.fabs((y[j]-y_new)/y[j])
           
    axes[j].semilogy(N, pogr, color="red")
    axes[j].set_xlabel('Число узлов')
    axes[j].set_ylabel('Относительная погрешность')
    axes[j].grid()
plt.show()