from typing import Union
from numpy import float32
import numpy as np
import numpy.typing as nt

# IIR

class System():
    def __init__(self,aa:nt.NDArray[float32],bb:nt.NDArray[float32]):
        if(aa.shape[0]!=bb.shape[0]+1):
            raise TypeError("Mismatched lengths. «aa»'s first dimension must be «bb».shape[0]+1")
        self.aa=aa
        self.bb=bb
        self.ww=np.zeros(aa.shape)
    def __call__(self,x:Union[float32,nt.NDArray[float32]]):
        self.ww = np.roll(self.ww,1,0)
        self.ww[0]=x+(self.bb*self.ww[1:]).sum()
        return (self.ww*self.aa).sum()
