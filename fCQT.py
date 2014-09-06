from __future__ import division
import math
import matplotlib.pyplot as plt
from tool.FFT import FFT
from tool.normalizer import max_normalize
from wav_in import wav_in
from tool.cqt import *

def Hanning(k,N):
    w = 0.5*(1-math.cos(2*math.pi*k/(N-1)))
    return w

def pre_process(signal):
    signal = max_normalize(signal)
    i=0
    while signal[i]<0.1 :
        signal[i] = 0
        i += 1
    signal = signal[:100000]
    return signal

def fCQT(name,pitch):
    print "processing\n"+name
    [signal,params] = wav_in(name)
    nchannels, sampwidth, framerate, nframes = params[:4]
    #print "orignal length:",len(signal)
    signal = pre_process(signal)
    #print "length now:",len(signal)
    #print params

    #signal = [signal[d*i] for i in range(int(len(signal)/d))]

    #constant in onset_detection
    h = int(2**math.ceil(math.log(framerate*0.03)/math.log(2))) # hop size
    #print "h=",h
    #print "time interval=",h/framerate,"s"
    N = 2*h # size of the Hanning window
    threshhold1 = 0.3 #standard
    threshhold2 = 0.2 #the lowest requirement for f_onset
    threshhold3 = 0.3 #to compensate for the decline of the requirement for f_onset, the local maximium must be greater than threshhold3


    M = int(len(signal)/h) -1
    L = int(N/2)
    wnd = [Hanning(i,N) for i in range(N)]

    """plt.plot(signal,"r")
    plt.show()"""


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

    nKey = len(seq_onset)

    fmin = 32.7
    fmax = 3951
    b_hop = 7 # 31 bins per note, 31 can be replaced by any other odd number. trade-off between effiency and accuracy
    bins = b_hop * 12
    rad = int(b_hop/2)
    drd = CQT(fmin,fmax,bins,framerate,hamming)
    F = [0]*nKey
    for j in range(nKey):
        i = seq_onset[j]
        """if (i>=2):
            print i,(i+1.0)/framerate*h
            x1 = drd.fast(signal[int((i-2)*h):int(i*h)])
            y1 = []
            for k in range(1,83):
                y1 += [sum(x1[k*b_hop-rad:k*b_hop+rad+1])/b_hop]
            y1 = max_normalize(y1)
        else :
            y1 = [0]*82"""
        
        if (i<=M-4):   
            print i,(i+1.0)/framerate*h
            x2 = drd.fast(signal[int((i+2)*h):int((i+4)*h)])
            y2 = []
            for k in range(1,83):
                y2 += [sum(x2[k*b_hop-rad:k*b_hop+rad+1])/b_hop]
            y2 = max_normalize(y2)
        else:
            y2 = [0]*82
            return ;
        
        F[j] = y2  #only consider the part after the onset

    file_object = open("train.dat","a")
    for i in range(nKey):
        file_object.write("%d " %pitch)
        for j in range(len(F[i])):
            if F[i][j]!=0:
                file_object.write(str(j+1)+":"+str(F[i][j])+" ")
        file_object.write("\n")
    file_object.close()
