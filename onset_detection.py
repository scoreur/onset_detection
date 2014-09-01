from __future__ import division
import math
import matplotlib.pyplot as plt
from tool.FFT import FFT
from tool.normalizer import max_normalize
from wav_in import wav_in




def Hanning(k,N):
    w = 0.5*(1-math.cos(2*math.pi*k/(N-1)))
    return w

def pre_process(signal):
    signal = max_normalize(signal)
    i=0
    while signal[i]<0.1 :
        signal[i] = 0
        i += 1
    signal = signal[:200000]
    return signal

name = raw_input("input the .wav file\n")
[signal,params] = wav_in(name)
nchannels, sampwidth, framerate, nframes = params[:4]
print "orignal length:",len(signal)
signal = pre_process(signal)
print "length now:",len(signal)
print params

#signal = [signal[d*i] for i in range(int(len(signal)/d))]

#constant in onset_detection
h = int(2**math.ceil(math.log(framerate*0.03)/math.log(2))) # hop size
print "h=",h
print "time interval=",h/framerate,"s"
N = 2*h # size of the Hanning window
threshhold1 = 0.3 #standard
threshhold2 = 0.2 #the lowest requirement for f_onset
threshhold3 = 0.3 #to compensate for the decline of the requirement for f_onset, the local maximium must be greater than threshhold3


M = int(len(signal)/h) -1
L = int(N/2)
wnd = [Hanning(i,N) for i in range(N)]

plt.plot(signal,"r")
plt.show()


print "calulating S..."  #  S stores the result of STFT of the signal
S = [[] for i in range(M)]

for m in range(M):
    x = [i*j for i,j in zip(signal[m*h:m*h+N],wnd)]
    S[m] = FFT(x)
        
S = map(lambda str:map(abs,str),S[:M])

print "calculating f and f_onset"

f = [0]*(M+1)
for m in range(M):
    f[m] = sum(S[m][1:int(len(S[m])/2)]) # f[m] is the sum of the magnitude spectrum
f = max_normalize(f);

f_onset = [0]*(M+1)
for m in range(1,M):
    if f[m] != 0.0:
        f_onset[m] = (f[m]-f[m-1])/f[m] #detection funtion
    else:
        f_onset[m] = 0
        

seq_onset = []        
for m in range(M):
    if (f_onset[m]>f_onset[m-1]) and (f_onset[m]>f_onset[m+1]) and ((f_onset[m]>threshhold1) or ((f_onset[m]>threshhold2) and (max(f[m-1:m+2])>threshhold3))):
        seq_onset += [m]
        
print [(i+1.0)/framerate*h for i in seq_onset]


"""time = [(i+0.5)/framerate*h for i in range(M+1)]

print "ploting"
plt.plot(time,f_onset,'r')
plt.plot(time,f,'b')
plt.xlabel("time")
plt.show()"""


