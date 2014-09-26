from __future__ import division
import math
import matplotlib.pyplot as plt
from tool.FFT import FFT
from tool.normalizer import max_normalize
from wav_in import wav_in
from tool.cqt import *
from libsvm.python.svmutil import *

compress = 1
note = ['C','bD','D','bE','E','F','bG','G','bA','A','bB','B']
dict = {'A':1,'Bb':2,'bB':2,'B':3,'C':-8,'bD':-7,'Db':-7,'D':-6,'bE':-5,'Eb':-5,'E':-4,'F':-3,'bG':-2,'Gb':-2,'G':-1,'bA':0,'Ab':0}
def Hanning(k,N):
    w = 0.5*(1-math.cos(2*math.pi*k/(N-1)))
    return w

def pre_process(signal,length):
    signal = max_normalize(signal)
    i=0
    while signal[i]<0.1 :
        signal[i] = 0
        i += 1
	l = int(len(signal)/compress)
    signal = [signal[compress*i] for i in range(l)]
    signal = signal[:length]
    return signal

def transfer_pitch(num):
    num = int(num)
    l = int((num+8) / 12)
    return note[(num+8) % 12]+str(l)
	
def fCQT(name,length=200000,compress=1):
    print "processing\n"+name
    [signal,params] = wav_in(name)
    nchannels, sampwidth, framerate, nframes = params[:4]
    framerate = int(nframerate/compress)
    #print "orignal length:",len(signal)
    signal = pre_process(signal,length)
    #print "length now:",len(signal)
    #print params

    #signal = [signal[d*i] for i in range(int(len(signal)/d))]

    #constant in onset_detection
    h = int(2**math.ceil(math.log(framerate*0.03)/math.log(2))) # hop size
    #print "h=",h
    #print "time interval=",h/framerate,"s"
    N = 2*h # size of the Hanning window
    threshhold1 = 0.5 #standard
    threshhold2 = 0.4 #the lowest requirement for f_onset
    threshhold3 = 0.6 #to compensate for the decline of the requirement for f_onset, the local maximium must be greater than threshhold3


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

	time = [(i+1.0)/framerate*h for i in seq_onset]		
    nKey = len(seq_onset)

    fmin = 32.7  #the 4th notes from the left
    fmax = 3951  #the 2nd notes from the right
    b_hop = 7 # 31 bins per note, 31 can be replaced by any other odd number. trade-off between effiency and accuracy
    bins = b_hop * 12
    rad = int(b_hop/2)
    drd = CQT(fmin,fmax,bins,framerate,hamming)
    F = [0]*nKey  
	
    for j in range(0,nKey):
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
			
        F[j] = y2  #only consider the part after the onset
		
		
    return (F,time)	

# important part ============================
def onset_svm(inputFile, modelFile, outputFile, length=200000,compress=1):
    [signal,params] = wav_in(inputFile)
    nchannels, sampwidth, nframerate, nframes = params[:4]
    
    framerate = int(nframerate/compress)
    #print "orignal length:",len(signal)
    signal = pre_process(signal,len(signal))
    #print "length now:",len(signal)
    #print params

    #signal = [signal[d*i] for i in range(int(len(signal)/d))]

    #constant in onset_detection
    h = int(2**math.ceil(math.log(framerate*0.03)/math.log(2))) # hop size
    #print "h=",h
    print "time interval=",h/framerate,"s"
    N = 2*h # size of the Hanning window
    threshhold1 = 0.5 #standard
    threshhold2 = 0.4 #the lowest requirement for f_onset
    threshhold3 = 0.6 #to compensate for the decline of the requirement for f_onset, the local maximium must be greater than threshhold3


    M = int(len(signal)/h) -1
    print "size of M", M
    L = int(N/2)
    wnd = [Hanning(i,N) for i in range(N)]

    """plt.plot(signal,"r")
    plt.show()"""


    print "calulating S..."  #  S stores the result of STFT of the signal
    #S = [[] for i in range(M)]
    f = [0]*(M+1)
    for m in range(M):
        print m
        S = FFT([i*j for i,j in zip(signal[m*h:m*h+N],wnd)])[1:L]
        S = map(abs, S[:])
        f[m] = sum(S)
    
    print "finish FFT"
#S = map(lambda str:map(abs,str),S[:M])
    # power spectrum

    print "calculating f and f_onset"


    '''for m in range(M):
        f[m] = sum(S[m][1:int(len(S[m])/2)]) '''# f[m] is the sum of the magnitude spectrum
    f = max_normalize(f);

    f_onset = [0]*(M+1)
    for m in range(1,M):
        if f[m] != 0.0:
            f_onset[m] = 1-f[m-1]/f[m] #detection funtion
        else:
            f_onset[m] = 0
        

    seq_onset = []        
    for m in range(M):
        if (f_onset[m]>f_onset[m-1]) and (f_onset[m]>f_onset[m+1]) and ((f_onset[m]>threshhold1) or ((f_onset[m]>threshhold2) and (max(f[m-1:m+2])>threshhold3))):
            seq_onset += [m]

	time = [(i+1.0)/framerate*h for i in seq_onset]		
    nKey = len(seq_onset)

    fmin = 32.7
    fmax = 3951
    b_hop = 7 # 31 bins per note, 31 can be replaced by any other odd number. trade-off between effiency and accuracy
    bins = b_hop * 12
    rad = int(b_hop/2)
    drd = CQT(fmin,fmax,bins,framerate,hamming)
    
    F = [0]*nKey  
	
    for j in range(0,nKey):
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
            F[j] = max_normalize(y2)
        else:
            F[j] = [0]*82
			
         #only consider the part after the onset
		
		
    y = [0]*len(F)
    
    fout = open(outputFile, 'w')
    for i in range(len(F)):
        for j in range(len(F[i])):
            fout.write(str(F[i][j])+' ')
        fout.write('\n')
    
    fout.close()
    print "finished"

	
    #modified by WYJ
    model = svm_load_model(modelFile);
    p_labels, p_acc, p_vals = svm_predict(y,F,model)
	
    #str_labels=[0]*len(y)
    str_labels = map(transfer_pitch, p_labels[:len(y)]);
    for i in range(len(time)):
        print str_labels[i],time[i]

    '''
    for i in range(len(y)):
       p_labels[i] = int(p_labels[i])
       str_labels[i] = transfer_pitch(int(p_labels[i]))'''


    return p_labels,str_labels,time