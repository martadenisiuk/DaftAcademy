import numpy as np
from math import pi
import scipy.stats
import matplotlib.pyplot as plt
import scipy
from scipy.integrate import quad

def funkcja1(x):
    return np.cos((pi * x) / 10) **  2 - 1/2

#Funkcja obliczająca całkę 
ans, err = np.abs(quad(funkcja1, 2.5, 7.5)) 

x1 = 2.5
x2 = 7.5
print(funkcja1(x1))
print(funkcja1(x2))

#Wykres tej funkcji

x = np.linspace(0, 10, 100)
y = funkcja1(x)


fig, ax = plt.subplots(figsize = (10,5))
plt.plot(x,y)
plt.ylim([-1,1])
plt.title('Wykres funkcji')
ax.set_aspect('equal')
ax.grid(True, which='both')

#aby były osie x i y w punkcie 0 
ax.spines['left'].set_position('zero')


ax.spines['right'].set_color('none')
ax.yaxis.tick_left()


ax.spines['bottom'].set_position('zero')


ax.spines['top'].set_color('none')
ax.xaxis.tick_bottom()
plt.show()

y1 = funkcja1((x1+x2)/2)
y2 = 0

print(y1)
print(y2)
print(ans)

N = 10000
pole = []
for j in range(0,N):
    X = np.random.uniform(x1,x2,N)
    Y = np.random.uniform(y1,y2,N)    
    p = 0
    z = 0
    for i in range(N):
        if Y[i] >= funkcja1(X[i]):
            p += 1
        else:
            z += 1
    pole.append((p / (p + z)) * (x2 - x1) * (y2 - y1))
#print(pole)
plt.hist(pole, bins='auto', color='#0504aa',
                            alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.title('Histogram')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()
print(np.mean(pole), np.std(pole))
normalny = scipy.stats.norm(np.mean(pole),np.std(pole))
print(scipy.stats.kstest(pole,normalny.cdf))
print(scipy.stats.ttest_1samp(pole, ans))