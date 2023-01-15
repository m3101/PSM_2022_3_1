
FSIZE = 100
FS = 44100

import os
import numpy as np

def h(fc1,fc2,fs):

    # w(fc=fs/2) = pi
    wc1 = ((2*fc1)/fs)*np.pi
    wc2 = ((2*fc2)/fs)*np.pi

    def h(n):
        if n==0:
            return (wc2-wc1)/np.pi
        else:
            return (np.sin(wc2*n)-np.sin(wc1*n))/(n*np.pi)
    return h


centres = np.array([32,64,128,256,512,1000,2000,4000,8000,16000])
cutoffs = (centres[1:]+centres[:-1])/2
cutoffs = np.concatenate(([0],cutoffs,[44100/2]))
print(cutoffs)

from matplotlib import pyplot as plt

def plotn(n):
    fig,axes = plt.subplots(2)
    if FSIZE%2==0:
        sampling_points = np.linspace(-(FSIZE-1)//2,FSIZE//2,FSIZE)
    else:
        sampling_points = np.linspace(-FSIZE//2,FSIZE//2,FSIZE)
    impresp = np.array([h(cutoffs[n],cutoffs[n+1],FS)(x) for x in sampling_points])

    with open(f"src/numpy/ufilter{n}.np","wb") as o_f:
        np.save(o_f,impresp)

    axes[0].plot(sampling_points,impresp,c="k")
    axes[0].set_xlabel("n")
    axes[0].set_ylabel("h[n]")

    to_transform = np.zeros((FS))
    to_transform[:FSIZE] = impresp
    transformed = 20*np.log(np.abs(np.fft.rfft(to_transform)))

    axes[1].plot(np.fft.rfftfreq(FS,1/FS)[:-1],transformed[:-1],c="k")
    axes[1].set_xlabel("f (Hz)")
    axes[1].set_ylabel("H[f] (dB)")

    plt.savefig(f"tex/fig/filter{n}.pdf")
    plt.close()

    return transformed

def b_nutall(x):
    return (
        0.3635819
        -0.4891775*np.cos(2*np.pi*x)
        +0.1365995*np.cos(4*np.pi*x)
        -0.0106411*np.cos(6*np.pi*x)
    )
def poisson(x,c=1):
    return np.exp(-np.abs(x)*c)
def plotnw(n):
    if FSIZE%2==0:
        sampling_points = np.linspace(-(FSIZE-1)//2,FSIZE//2,FSIZE)
    else:
        sampling_points = np.linspace(-FSIZE//2,FSIZE//2,FSIZE)
    impresp = np.array([h(cutoffs[n],cutoffs[n+1],FS)(x) for x in sampling_points])

    x=(
        (sampling_points-sampling_points.min())
        /(sampling_points.max()-sampling_points.min())
    )
    impresp = impresp*b_nutall(x) * poisson(2*(x-.5))

    with open(f"src/numpy/filter{n}.np","wb") as o_f:
        np.save(o_f,impresp)

    if not os.path.exists("tex/fig/window.pdf"):
        fig,axes = plt.subplots(2)
        axes[0].plot(sampling_points,b_nutall(x)*poisson(2*(x-.5)),c='k')
        axes[0].set_xlabel("n")
        axes[0].set_ylabel("w[n]")

        to_transform = np.zeros((FS))
        to_transform[:FSIZE] = b_nutall(x)*poisson(2*(x-.5))
        transformed = 20*np.log(np.abs(np.fft.fft(to_transform)))

        axes[1].plot(np.fft.fftshift(np.fft.fftfreq(FS,1/FS))[10:],np.fft.fftshift(transformed)[10:],c="k")
        axes[1].set_xlabel("f (Hz)")
        axes[1].set_ylabel("H[f] (dB)")
        plt.savefig("tex/fig/window.pdf")
        plt.close()
    
    fig,axes = plt.subplots(2)
    axes[0].plot(sampling_points,impresp,c="k")
    axes[0].set_xlabel("n")
    axes[0].set_ylabel("h[n]")

    to_transform = np.zeros((FS))
    to_transform[:FSIZE] = impresp
    transformed = 20*np.log(np.abs(np.fft.rfft(to_transform)))

    axes[1].plot(np.fft.rfftfreq(FS,1/FS)[:-1],transformed[:-1],c="k")
    axes[1].set_xlabel("f (Hz)")
    axes[1].set_ylabel("H[f] (dB)")

    plt.savefig(f"tex/fig/windowfilter{n}.pdf")
    plt.close()

    return transformed

# [plotn(n) for n in range(10)]
# [plotnw(n) for n in range(10)]

DISCARD=-1000

filter = np.zeros((FSIZE))
for i in range(10):
    with open(f"src/numpy/filter{i}.np",'rb') as i_f:
        filter+=np.load(i_f)
to_transform = np.zeros((FS))
to_transform[:FSIZE]=filter
transformed = 20*np.log(np.abs(np.fft.rfft(to_transform)))
plt.figure()
plt.plot(np.fft.rfftfreq(FS,1/FS)[:DISCARD],transformed[:DISCARD],c="k")
plt.xlabel("f (Hz)")
plt.ylabel("H[f] (dB)")
plt.savefig("tex/fig/windowed.pdf")
plt.close()

filter = np.zeros((FSIZE))
for i in range(10):
    with open(f"src/numpy/filter{i}.np",'rb') as i_f:
        filter+=np.load(i_f)*(2**i)*(0 if i%2==0 else 1)
to_transform = np.zeros((FS))
to_transform[:FSIZE]=filter
transformed = 20*np.log(np.abs(np.fft.rfft(to_transform)))
plt.figure()
plt.plot(np.fft.rfftfreq(FS,1/FS)[:DISCARD],transformed[:DISCARD],c="k")
plt.xlabel("f (Hz)")
plt.ylabel("H[f] (dB)")
plt.savefig("tex/fig/windowed_stair.pdf")
plt.close()

filter = np.zeros((FSIZE))
for i in range(10):
    with open(f"src/numpy/ufilter{i}.np",'rb') as i_f:
        filter+=np.load(i_f)
to_transform = np.zeros((FS))
to_transform[:FSIZE]=filter
transformed = 20*np.log(np.abs(np.fft.rfft(to_transform)))
plt.figure()
plt.plot(np.fft.rfftfreq(FS,1/FS)[:DISCARD],transformed[:DISCARD],c="k")
plt.xlabel("f (Hz)")
plt.ylabel("H[f] (dB)")
plt.savefig("tex/fig/nowindow.pdf")
plt.close()

filter = np.zeros((FSIZE))
for i in range(10):
    with open(f"src/numpy/ufilter{i}.np",'rb') as i_f:
        filter+=np.load(i_f)*(2**i)*(0 if i%2==0 else 1)
to_transform = np.zeros((FS))
to_transform[:FSIZE]=filter
transformed = 20*np.log(np.abs(np.fft.rfft(to_transform)))
plt.figure()
plt.plot(np.fft.rfftfreq(FS,1/FS)[:DISCARD],transformed[:DISCARD],c="k")
plt.xlabel("f (Hz)")
plt.ylabel("H[f] (dB)")
plt.savefig("tex/fig/nowindow_stair.pdf")
plt.close()