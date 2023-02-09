
FSIZE = 1000
FS = 44100

import os
import numpy as np

def sample_fourier(x,f):
    return np.sum(x*np.exp((f/FS)*1j*np.linspace(0,1,len(x))))

def h(fc1,fc2,fs):

    # w(fc=fs/2) = pi
    wc1 = ((2*fc1)/fs)*np.pi
    wc2 = ((2*fc2)/fs)*np.pi

    wc1 = wc1 if wc1<np.pi else np.pi
    wc2 = wc2 if wc2<np.pi else np.pi

    def h(n):
        if n==0:
            return (wc2-wc1)/np.pi
        else:
            return (np.sin(wc2*n)-np.sin(wc1*n))/(n*np.pi)
    return h


centres = np.array([32,64,128,256,512,1000,2000,4000,8000,16000])
cutoffs = (centres[1:]+centres[:-1])/2
cutoffs = np.concatenate(([0],cutoffs,[1.5*44100/2]))
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
    transformed = 20*np.log10(np.abs(np.fft.rfft(to_transform)))

    axes[1].plot(np.fft.rfftfreq(FS,1/FS)[:-1],transformed[:-1],c="k")
    axes[1].set_xlabel("f (Hz)")
    axes[1].set_xlim(0,500 if n<=4 else 20000)
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

def hamming(x):
    return 0.54-.46*np.cos(2*np.pi*x)

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
    # f=b_nutall(x)*poisson(1*(x-.5))
    f = hamming(x)
    impresp = impresp*f

    if not os.path.exists("tex/fig/window.pdf"):
        fig,axes = plt.subplots(2)
        axes[0].plot(sampling_points,f,c='k')
        axes[0].set_xlabel("n")
        axes[0].set_ylabel("w[n]")

        to_transform = np.zeros((FS))
        to_transform[:FSIZE] = f
        transformed = 20*np.log10(np.abs(np.fft.fft(to_transform)))

        axes[1].plot(
            np.fft.fftshift(np.fft.fftfreq(FS,1/FS))[10:],
            np.fft.fftshift(transformed)[10:],
            c="k"
        )
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
    transform = np.abs(np.fft.rfft(to_transform))
    impresp*= 1/transform.max()

    with open(f"src/numpy/filter{n}.np","wb") as o_f:
        np.save(o_f,impresp)
    
    to_transform[:FSIZE] = impresp
    transform = np.abs(np.fft.rfft(to_transform))
    transformed = 20*np.log10(transform)

    axes[1].plot(np.fft.rfftfreq(FS,1/FS)[:-1],transformed[:-1],c="k")
    axes[1].set_xlim(0,500 if n<=4 else 20000)
    axes[1].set_ylim(-100,0)
    axes[1].set_xlabel("f (Hz)")
    axes[1].set_ylabel("H[f] (dB)")
    axes[1].text(.5,.5,f"Max: {transformed.max()}dB")

    plt.savefig(f"tex/fig/windowfilter{n}.pdf")
    plt.close()

    return transformed

[plotn(n) for n in range(10)]
[plotnw(n) for n in range(10)]

DISCARD=-1000

filter = np.zeros((FSIZE))
for i in range(10):
    with open(f"src/numpy/filter{i}.np",'rb') as i_f:
        filter+=np.load(i_f)
to_transform = np.zeros((FS))
to_transform[:FSIZE]=filter
transformed = 20*np.log10(np.abs(np.fft.rfft(to_transform)))
plt.figure()
plt.plot(np.fft.rfftfreq(FS,1/FS)[:DISCARD],transformed[:DISCARD],c="k")
plt.xlabel("f (Hz)")
plt.ylabel("H[f] (dB)")
plt.ylim(-10,10)
plt.savefig("tex/fig/windowed.pdf")
plt.close()

filter = np.zeros((FSIZE))
for i in range(10):
    with open(f"src/numpy/filter{i}.np",'rb') as i_f:
        filter+=np.load(i_f)*(2**i)*(0 if i%2==0 else 1)
to_transform = np.zeros((FS))
to_transform[:FSIZE]=filter
transformed = 20*np.log10(np.abs(np.fft.rfft(to_transform)))
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
transformed = 20*np.log10(np.abs(np.fft.rfft(to_transform)))
plt.figure()
plt.plot(np.fft.rfftfreq(FS,1/FS)[:DISCARD],transformed[:DISCARD],c="k")
plt.ylim(-10,10)
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
transformed = 20*np.log10(np.abs(np.fft.rfft(to_transform)))
plt.figure()
plt.plot(np.fft.rfftfreq(FS,1/FS)[:DISCARD],transformed[:DISCARD],c="k")
plt.xlabel("f (Hz)")
plt.ylabel("H[f] (dB)")
plt.savefig("tex/fig/nowindow_stair.pdf")
plt.close()