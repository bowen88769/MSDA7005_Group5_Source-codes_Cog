import numpy as np
from scipy.optimize import fsolve
from math import gamma
import matplotlib.pyplot as plt
from scipy.stats import norm
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

n = 8
B = 1 ###prompt
m = 3
conj_err = 0.914
thre = 0.05
klist = []
errlist = []
paralist = []
poss_para = []

def new_gamma(x):
    if x<1:
        result = 1
    else:
        result = gamma(x)
    return result

def compute_err(n,k,q,m):
    k = k+1
    front = (gamma(k)*gamma(n-k))/(gamma(n))
    summ = 0 
    for a in range(0,m+1):
        item1 = (new_gamma(m))/(new_gamma(a)*new_gamma(m-a))
        item2 = (new_gamma(n-m))/(new_gamma(n-m-k+a)*new_gamma(k-a))
        item3 = a*q
        summ = summ + item1*item2*item3
    value = front*summ
    return value
    
###numerical solution and parameters mattching
for r in range(-30,0):
    for u in range(-30,30):
        for q in range(0,100):
            r = r/30
            u = u/30
            q = q/100
            def func(k,n=n,B=B,r=r,u = u):
                return np.log((n/k)-1)-(2/n)*r*k-B*u
            k = float(fsolve(func,0.1))
            if k>m:
                err = compute_err(n,k,q,m)
                klist.append(k)
                errlist.append(err)
                paralist.append([r,u,q])
            
for i in range(len(klist)):
    if abs(errlist[i]-conj_err)<thre:
        poss_para.append(paralist[i])
        
possr = [item[0] for item in poss_para]
possu = [item[1] for item in poss_para]
possq = [item[2] for item in poss_para]

###visualization of reliable parameters' values
plt.hist(possr,density = True)
plt.title('Density of possible_r')
data = pd.Series(possr)
data.plot(kind = 'kde',label = '密度图') 

plt.hist(possu,density = True)
plt.title('Density of possible_u')
data = pd.Series(possu)
data.plot(kind = 'kde',label = '密度图') 
plt.show()

plt.hist(possq,density = True)
plt.title('Density of possible_q')
data = pd.Series(possq)
data.plot(kind = 'kde',label = '密度图') 

###the solution of error rate under q=0.5
rlist2 = []  ###parameters denoting the prompt activation sensitivity
ulist2 = []  ###parameters denoting the degree of LLMs' inertness in inference tasks
errlist2 = []
for r in range(-30,0):
    for u in range(-30,30):
        r = r/30
        u = u/30
        q=0.5
        def func(k,n=n,B=B,r=r,u = u):
            return np.log((n/k)-1)-(2/n)*r*k-B*u
        k = float(fsolve(func,0.1))
        if k>m:
            err = compute_err(n,k,q,m)
            if err>=0 and err<=1:
                rlist2.append(r)
                ulist2.append(u)
                errlist2.append(err)
                
data = pd.DataFrame({"r_value":rlist2,
                     "u_value":ulist2,
                     "err_value":errlist2})

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(data['r_value'], data['u_value'],data['err_value'])
ax.set_xlabel('r_value')
ax.set_ylabel('u_value')
ax.set_zlabel('error_value')
ax.set_title('Error Rates under different parameters')
plt.show()

