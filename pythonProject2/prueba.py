import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import sounddevice as sd
from os import mkdir

directorio='C:\\Users\\Ana Cuevas de Cózar\\PycharmProjects\\pythonProject2\\PruebaAnexo2\\'
mkdir(directorio)
SR = 44100  # sample rate (Hz)
f0 = 441  # fundamental frequency (Hz)
TF = 1  # duration of simulation (s)
ctr = 0.7  # center location/width of excitation
wid = 0.1  # center location/width of excitation
u0 = 1  # maximum initial displacement
v0 = 0  # maximum initial velocity
rp = 0.3  # position of readout (0-1)

# Derived parameters
k = 1 / SR  # time step
NF = int(SR * TF)  # duration of simulation (samples)
N = int(0.5 * SR / f0)  # length of delay lines
rp_int = 1 + int(N * rp)  # rounded grid index for readout
rp_frac = 1 + rp * N - rp_int  # fractional part of readout location

# Initialize delay lines and output
wleft = np.zeros(N)
wright = np.zeros(N)
out = np.zeros(NF)

# Create raised cosine and integral
xax = (np.arange(1, N + 1) - 1 / 2) / N
ind = np.sign(np.maximum(-(xax - ctr - wid / 2) * (xax - ctr + wid / 2), 0))
rc = 0.5 * ind * (1 + np.cos(2 * np.pi * (xax - ctr) / wid))
rcint = np.zeros(N)
for qq in range(1, N):
    rcint[qq] = rcint[qq - 1] + rc[qq] / N

# Set initial conditions
wleft = 0.5 * (u0 * rc + v0 * rcint / (2 * f0))
wright = 0.5 * (u0 * rc - v0 * rcint / (2 * f0))

# Start main loop
for n in range(2, NF+1):
    temp1 = wright[N - 1]
    temp2 = wleft[0]
    wright[1:N] = wright[0:N - 1]
    wleft[0:N - 1] = wleft[1:N]
    wright[0] = -temp2
    wleft[N - 1] = -temp1
    plt.plot(range(0, N), wleft, 'r')
    plt.plot(range(0, N), wright, 'b')
    #plt.plot(range(0, N), wleft+wright, 'k')
    plt.xlabel('x')
    plt.ylabel('u')
    plt.title(f'Cuerda en el instante {n}')
    plt.savefig(directorio + f'Cuerda_instante_{n}.png')
    plt.close()
    # Readout
    out[n] = (1 - rp_frac) * (wleft[rp_int] + wright[rp_int]) + rp_frac * (wleft[rp_int + 1] + wright[rp_int + 1])


# Plot output waveform
plt.plot(np.arange(NF) * k, out, 'k')
plt.xlabel('t')
plt.ylabel('u')
plt.title('1D Wave Equation: Digital Waveguide Synthesis Output')
plt.axis('tight')
plt.show()

# Save sound to a WAV file
out_normalized = out / np.max(np.abs(out))
write('output.wav', SR, out_normalized.astype(np.float32))

# Play sound
sd.play(out_normalized, SR)
sd.wait()

