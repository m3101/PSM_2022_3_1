import os
import numpy as np
n=100
exp = (np.e**(-np.linspace(0,1,n)))
# exp = np.zeros((n))
# exp[0]=1

exp/=exp.sum()
with open(os.environ["PSM_PIPE"],'wb') as f:
    print("OPEN")
    print(f.write(exp.astype(np.float32).tobytes()))