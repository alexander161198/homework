import numpy as np
import matplotlib.pyplot as plt

r_norm = []

def conjugate_gradient(A, b, C_inv, eps):
    
    x = np.zeros(len(b))
    M_obuslavl = np.dot(np.dot(C_inv, A), C_inv.transpose())
    # print(linalg.norm(A) * linalg.norm(np.matrix(A).I))
    r = b - np.dot(M_obuslavl, x)
    alpha = sum(r[i] ** 2 for i in range(len(r)))
    
    r1 = r
    for i in range(len(b)):
        u = np.dot(M_obuslavl, r1)
        t = alpha / (sum(r1[j] * u[j] for j in range(len(u))))
        x = x + t * r1
        r = r - t * u
        
        r_norm.append(np.linalg.norm(r))
            
        betta = sum(r[j] ** 2 for j in range(len(r)))
        
        if np.linalg.norm(r) < eps:
            return x

        s = betta / alpha
        r1 = r + s * r1
        alpha = betta
        
        
def plot_lines (x, y, T):
    k = 0
    T_matrix = np.zeros((len(x),len(x)))
    for i in range (len(x)):
        for j in range (len(x)):
            T_matrix[i][j] = T[k]
            k += 1       

    plt.xlabel('x')
    plt.ylabel('y')
    plt.contourf(x, y, T_matrix)
    plt.colorbar()
    plt.show()


def plot_norm ():
    fig, ax = plt.subplots(figsize=(12,8))
    ax.plot(r_norm, label="норма вектора")
    ax.set_yscale('log')
    ax.set_ylabel('Значение нормы', fontsize=14)
    ax.set_xlabel('Номер итерации', fontsize=14)
    ax.legend(fontsize=14)
    ax.grid()
    plt.show()
    
    
    
N = 18 
h = 1/(N-1)
x = [k*h for k in range (0, N)]
y = [k*h for k in range (0, N)]

M = np.zeros((N**2,N**2))
R = np.zeros(N**2)
T = np.zeros(N**2)

for i in range (N):
    for j in range (N):
        
        if i==0 or j==0 or i==N-1 or j==N-1:
            M[j+N*i][j+N*i] = 1
            R[j+N*i]=0
            continue
        M[j+N*(i)][j+N*(i)] = 1;#i,j
    
        if i!=0 and j!=0 and i!=N-1 and j!=N-1:
            M[j+N*(i)][j+N*(i+1)] = -1/(h**2) #i+1, j
            M[j+N*(i)][j+N*(i)] = 4/(h**2)#i,j
            M[j+N*(i)][j+N*(i-1)] = -1/(h**2)#i-1, j,
            M[j+N*(i)][j+N*(i)+1] = -1/(h**2)#i,j+1
            M[j+N*(i)][j+N*(i)-1] = -1/(h**2)#i,j-1
            R[j+N*(i)] = 1
            continue
        M[j+N*(i)][j+N*(i)] = 1;#i,j


index = []     
T = np.linalg.inv(M).dot(R)
T=np.round(T,10)
for l in range (N**2):
    if T[l]==0.:
        index.append(l)
        
T_new = np.delete(T,index)
R_new = np.delete(R, index)
M_new = np.delete(M,index,0)
M_new = np.delete(M_new,index,1)

eps=0.0001   
#C = np.eye(len(T_new))
#T_new = conjugate_gradient(M_new, R_new, C, eps)

C = np.eye(len(T))
#T = conjugate_gradient(M, R, C, eps)
#plot_lines(x, y, T)
#plot_norm()

for i in range (N**2):
     C[i][i] = 1/np.sqrt(M[i][i])

T = conjugate_gradient(M, R, C, eps)
plot_norm()
