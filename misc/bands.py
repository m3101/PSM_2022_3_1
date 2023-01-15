import numpy as np
from matplotlib import pyplot as plt

def repeat(x):
    def yielder():
        while True:
            yield x
    return yielder()

centres = np.array([32,64,128,256,512,1000,2000,4000,8000,16000])
cutoffs = (centres[1:]+centres[:-1])/2
cutoffs = np.concatenate(([0],cutoffs,[44100/2]))

print(cutoffs)

fig,ax = plt.subplots(1,1,constrained_layout=True)
ax.set_yticks([])
ax.set_xlabel("Frequência (hz)")

n=6

ax.vlines(centres,0,.5,"k","dotted")
for t,p in zip([str(x)+"hz" for x in centres[n:]],list(zip(centres[n:],repeat(.5)))):
    ax.annotate(t,p).set_rotation(45)

ax.vlines(cutoffs,0,1,"k","solid")
for t,p in zip([str(int(x))+"hz" for x in cutoffs[n:]],list(zip(cutoffs[n:],repeat(1)))):
    ax.annotate(t,p)

ax.set_visible(True)
plt.show()
print(cutoffs)