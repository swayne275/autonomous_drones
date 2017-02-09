'''
Author: Stephen Wayne
This file exists mostly to test features that I add to the rxSDR class

Can now smell radio waves. Plots speed improved by 2-3x.
1/24:    changed freq range to BW around center freq so useful to scan
1/26:    adding ability to print to a file
'''

PLOT = False

import sdrClass
if PLOT:
    import matplotlib.pyplot as plt
    plt.close('all')
import numpy as np
import time
import drone_control

np.set_printoptions(precision=4)

fcLow = 30
fcHigh = 50
fs = 2.5
bw = 300
gain = 'auto'
NFFT = 1024
SAVE = True
FILENAME = "fullRange_2_5mhz.txt"
NUM_DECIMAL = 3
SCAN_RES = 1

radio = sdrClass.rxSDR(30, fs, bw, gain)  # radio on RPi
Pilot = drone_control.Pilot(True, True, True)

fc_list = np.linspace(fcLow, fcHigh, ((fcHigh - fcLow)/(SCAN_RES*fs) + 1))

# this plots the data 2-3x faster than usual. useful for obs. single freq
if PLOT:
    plt.clf();
    plt.ion()                             # turn on interactive plotting
    fLow = -0.5*fs
    fHigh = 0.5*fs                        # plot BW to scan many freqs
    f = np.linspace(fLow, fHigh, NFFT)
    fig, ax= plt.subplots()
    line, = ax.plot(np.random.randn(100))
    plt.title("Spectrum at fc=" + str(fcLow) + ", fs=" + str(fs*1000) + " khz")
    plt.ylabel("magnitude (dB)")
    plt.xlabel("frequency bin")
    plt.xlim(fLow, fHigh)                     # observe entire bandwidth
    plt.ylim(-30, 30)                         # sets plot dynamic range, in dB
    plt.show(block=False)
    line.set_xdata(f)
if SAVE:
    with open(FILENAME, 'a') as file:
        file.write('fl,%f,fh,%f,fs,%f,mhz,gain,%s,nfft,%d,scan,%f'%(fcLow,fcHigh,fs,gain,NFFT,SCAN_RES)+'\n')
now = time.time()
for x in fc_list:
    radio.setFc(x, "mhz")
    if ((time.time() - now) < 0.025): time.sleep(0.025 - (time.time()-now)) # allow PLL to settle
    freqs = radio.getFrequencies(NFFT)
    if PLOT:
        line.set_ydata(freqs)
        plt.title("Spectrum at f=" + str(x) + ", fs=" + str(fs*1000) + " khz")
        fig.canvas.draw()
        fig.canvas.flush_events()
    if SAVE:
        with open(FILENAME, 'a') as f:
            f.write(','.join(map(str, np.round(freqs, NUM_DECIMAL))) + '\n')
print("Scan required " + str(time.time() - now) + " seconds")
