import os
import numpy as np
n=50
x=np.linspace(0,1,n)
exp = (np.e**(-x))
exp = exp*np.cos(x*np.pi*3)
# exp = np.zeros((n))
# exp[0]=1
exp/=exp.sum()

from matplotlib import pyplot as plt

plt.scatter(x,exp)
plt.show()

with open(os.environ["PSM_PIPE"],'wb') as f:
    print("OPEN")
    print(f.write(exp.astype(np.float32).tobytes()))