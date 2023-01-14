import system
import numpy as np
from matplotlib import pyplot as plt

oxx = np.linspace(0,1,10)
impulseresp = np.e**(-oxx)

testsys = system.System(impulseresp,impulseresp[1:]/10)

xx = list(range(100))
plt.plot(oxx,impulseresp)
plt.figure()
plt.plot(xx,[testsys(1 if x==0 else 0) for x in xx])
plt.show()
