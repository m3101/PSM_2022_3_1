import numpy as np
import math

def taylor(x,fs):
    return sum([(f*((x-1)**i))/math.factorial(i) for i,f in enumerate(fs)])
values=[0.0644388205592, -0.0071041113165, -0.0068147306047, 0.0008603822712, 0.0008217417013, -0.0001148130927, -0.0001092937666, 0.0000163920811, 0.0000155662679, -0.0000024517914, -0.0000023241318, 0.0000003789182, 0.0000003587092, -0.0000000599726, -0.0000000567156, 0.0000000096642, 0.0000000091319, -0.0000000015793, -0.0000000014913, 0.000000000261, 0.0000000002463]

n=20
x=np.linspace(-n,n,2*n)
y=(np.sin(0.427427571917*x)-np.sin(0.2137137859585*x))/(np.pi*x)
y[0]=(0.427427571917-0.2137137859585)/np.pi

def approx(n,xx):
    return np.array([taylor(x,values[:n]) for x in xx])

from matplotlib import pyplot as plt

plt.plot(x,y)
plt.plot(x,approx(20,x))
plt.show()

print(np.sum((approx(20,x)-y)**2)**.5)