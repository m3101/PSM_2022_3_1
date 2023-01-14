import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl

S=4096
gg=2**np.array(range(1,11))
ww=np.array(range(1,500))
M=10

G,W = np.meshgrid(gg,ww)

L=S/G

multis_fft = S*W+G*((L/2)*np.log2(L))
multis_niv = S*W*M
multis_fft_melhor = multis_fft<multis_niv

somas_fft = S*W+G*(L*np.log2(L)+L)
somas_niv = S*M*(W+3)
somas_fft_melhor = somas_fft<somas_niv

rmulti = multis_niv/multis_fft
print(rmulti.mean())
print(rmulti.max())
print(rmulti.min())

rsomas = somas_niv/somas_fft
print(rsomas.mean())
print(rsomas.max())
print(rsomas.min())

# plt.title("Multiplicaçõs: FFT - Acumulador")
# plt.xlabel("G")
# plt.ylabel("W")
# plt.imshow(
#     multis_fft-multis_niv,
#     norm=mpl.colors.CenteredNorm(),
#     cmap="seismic",
#     aspect='auto',
#     interpolation="none",
#     extent=(1,11,1,500),
#     origin="lower"
# )
# plt.figure()
# plt.xlabel("G")
# plt.ylabel("W")
# plt.title("Somas: FFT - Acumulador")
# plt.imshow(
#     somas_fft-somas_niv,
#     norm=mpl.colors.CenteredNorm(),
#     cmap="seismic",
#     aspect='auto',
#     interpolation="none",
#     extent=(1,11,1,500),
#     origin="lower"
# )
# plt.show()